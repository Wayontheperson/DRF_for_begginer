from rest_framework import serializers
from .models import Amenity,Room



class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "id",
            "name",
            "descriptions",
        ) 