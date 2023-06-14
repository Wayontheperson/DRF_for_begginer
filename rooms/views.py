from .models import Amenity, Room
from . import serializers
from categories.models import Category

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    NotAuthenticated,
)


class Amenities(APIView):
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
    def get(self, request):
        rooms = Room.objects.all()
        serializer = serializers.RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
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
                updated_room = serializer.save(owner=request.user, category=category)
                # Amenity is a many_to_many field
                # how to work with many_to_many field
                amenities = request.data.get("amenities")
                for amenity_pk in amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                    except Amenity.DoesNotExist:
                        updated_room.delete()
                        raise ParseError(f"Amenity with id {amenity_pk} not found")
                    # many_to_many field can add object using "add" method
                    # foreign key can't do "add"
                    updated_room.amenities.add(amenity)
                serializer = serializers.RoomDetailSerializer(updated_room)
                return Response(serializer.data)
            else:
                return Response(serializer.errors,
                                status=HTTP_400_BAD_REQUEST)
        else:
            raise NotAuthenticated

class RoomsDetail(APIView):
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

