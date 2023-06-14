from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "descriptions",
        )


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class RoomDetailSerializer(serializers.ModelSerializer):
    # read_only 선언시 validated_data로 받을 수 없다.
    owner = TinyUserSerializer(read_only=True )
    amenities = AmenitySerializer(read_only=True,many=True,)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
