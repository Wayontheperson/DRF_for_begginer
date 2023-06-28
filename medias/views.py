from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_200_OK

from .models import Photo


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def _get_object(self, pk: int) -> Photo:
        return get_object_or_404(Photo, pk=pk)

    def delete(self, request, pk: int):
        photo = self._get_object(pk)
        if (photo.room and photo.room.owner != request.user) or (
                photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)
