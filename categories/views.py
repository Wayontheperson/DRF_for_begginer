from .models import Category
from .serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import (
    NotFound,
)

class Categories(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        new_data = request.data
        serializer = CategorySerializer(data=new_data)
        if serializer.is_valid():
            new_category = serializer.save()

            return Response(serializer.data)
        else:
            return HTTP_400_BAD_REQUEST

class CategoryDetail(APIView):
    def _get_object(self, pk):
        try:
            obj = Category.objects.get(id=pk)
            return obj
        except Category.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):   
        category = self._get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        categories = self._get_object(pk)
        serializer = CategorySerializer(
            categories,
            data = request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_data = serializer.save()
            return Response(CategorySerializer(updated_data).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        delete_data = self._get_object(pk)
        delete_data.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    


