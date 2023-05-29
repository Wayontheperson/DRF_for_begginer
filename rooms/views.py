from rest_framework.views import APIView
from .models import Amenity, Room
from . import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
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
            return Response(
                serializers.AmenitySerializer(amenity).data
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

class AmedityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(id=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self,request, pk):
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
            return Response(
                serializers.AmenitySerializer(updated_amenity).data
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )
        
    def delete(self,pk):
        delete_item = self.get_object(pk)
        delete_item.delete()
        return Response(status=HTTP_204_NO_CONTENT)

