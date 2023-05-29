from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import PerkSerializer
from .models import Perk


class Perks(APIView):
    def get(self, request):
        try:
            return Response(PerkSerializer(Perk.objects.all(), many=True).data)

        except Perk.DoesNotExist:
            raise HTTP_404_NOT_FOUND

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerksDetail(APIView):
    def _get_object(self, pk):
        try:
            data = Perk.objects.get(id=pk)
            return data
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self._get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self._get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(PerkSerializer(updated).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self._get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
