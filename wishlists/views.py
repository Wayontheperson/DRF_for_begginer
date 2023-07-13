from django.shortcuts import get_object_or_404

from rest_framework.status import HTTP_204_NO_CONTENT,HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rooms.models import Room
from .models import Wishlist
from .serializers import WishlistSerializer


class Wishlists(APIView):
    def get(self, request):
        all_wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlist,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(request.data)
        if serializer.is_valid():
            new_wishlist = serializer.save(user=request.user)
            serializer = WishlistSerializer(new_wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistsDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        wishlist = get_object_or_404(Wishlist, pk=pk, user=user)
        return wishlist

    def get(self, request, pk):
        wishlist = self.get_object(pk=pk, user=request.user)
        serializer = WishlistSerializer(wishlist, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        updating_data = self.get_object(pk=pk, user=request.user)
        serializer = WishlistSerializer(
            updating_data,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_data = serializer.save()
            serializer = WishlistSerializer(
                updated_data,
                context={"request": request}
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        removing_data = self.get_object(pk=pk, user=request.user)
        removing_data.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class WishlistToggle(APIView):
    def get_list(self, pk, user):
        return get_object_or_404(Wishlist, pk=pk, user=user)

    def get_room(self, pk):
        return get_object_or_404(Room, pk=pk)

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room_pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)
