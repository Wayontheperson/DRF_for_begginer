from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    NotAuthenticated,
)

from . import serializers
from .models import Amenity, Room
from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhothSerializer


class Amenities(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = serializers.AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(serializers.AmenitySerializer(amenity).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenityDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Amenity.objects.get(id=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = serializers.AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = serializers.AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(serializers.AmenitySerializer(updated_amenity).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, pk):
        delete_item = self.get_object(pk)
        delete_item.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = serializers.RoomListSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.RoomDetailSerializer(data=request.data)
        # read_only 필드는 validated_data로 넘어가지 않는다
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")

            try:
                with transaction.atomic():

                    updated_room = serializer.save(owner=request.user, category=category)
                    # Amenity is a many_to_many field
                    # how to work with many_to_many field
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        updated_room.amenities.add(amenity)
                    serializer = serializers.RoomDetailSerializer(updated_room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors,
                            status=HTTP_400_BAD_REQUEST)



class RoomsDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _get_object(self, pk):
        try:
            room = Room.objects.get(id=pk)
            return room
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self._get_object(pk)
        serializer = serializers.RoomDetailSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        room = self._get_object(pk)
        serializer = serializers.RoomDetailSerializer(room,
                                                      data=request.data,
                                                      partial=True)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            try:
                category = Category.objects.get(pk=category_pk)
                if not category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be 'rooms'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            amenities = request.data.get("amenities")
            if amenities is not None:
                try:
                    with transaction.atomic():
                        updated_room = serializer.save(owner=request.user, category=category)
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            updated_room.amenities.add(amenity)
                        serializer = serializers.RoomDetailSerializer(updated_room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
            else:
                updated_room = serializer.save(owner=request.user, category=category)
                serializer = serializers.RoomDetailSerializer(updated_room)
                return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        room = self._get_object(pk)
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self._get_object(pk)
        serializer = ReviewSerializer(room.reviews.all()[start:end],  # db에 가져온뒤 슬라이싱 하는게 아니라 슬라이싱 정보로 db heat
                                      many=True)
        return Response(serializer.data)

    def post(self, requset, pk):
        serializer = ReviewSerializer(data=requset.data)
        if serializer.is_valid():
            review = serializer.save(
                user=requset.user,
                room=self._get_object(pk)
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _get_objcet(self,pk):
        return get_object_or_404(Room, pk=pk)

    def post(self, request, pk):
        room = self._get_objcet(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhothSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhothSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
