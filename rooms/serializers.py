from rest_framework import serializers

from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhothSerializer
from wishlists.models import Wishlist


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
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True, )
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    photos = PhothSerializer(many=True, read_only=True)
    is_host = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_host(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user,
                                       rooms__pk=room.pk,  # manytomany relationship lookups across relationships
                                       ).exists()


class RoomListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    photos = PhothSerializer(many=True, read_only=True)
    is_host = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "photos",
            "is_host",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_host(self, room):
        request = self.context["request"]
        return room.owner == request.user
