from rest_framework.serializers import ModelSerializer
from .models import Photo

class PhothSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )

