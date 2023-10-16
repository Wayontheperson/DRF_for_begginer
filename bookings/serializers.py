from django.utils import timezone

from rest_framework import serializers
from .models import Bookings


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests"
        )


class CreateBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Bookings
        fields = (
            "guests",
            "check_in",
            "check_out",
        )

    def validate_check_in(self, data):
        now = timezone.localdate()
        if now > data:
            raise serializers.ValidationError("Can't book in the past")
        return data

    def validate_check_out(self, data):
        now = timezone.localtime(timezone.now()).date()
        if now > data:
            raise serializers.ValidationError("Can't book in the past!")
        return data

    def validate(self, data):
        room = self.context.get("room")
        if data["check_in"] >= data["check_out"]:
            raise serializers.ValidationError(
                "Check in should be before Check out"
            )
        if Bookings.objects.filter(
                room=room,
                check_in__lt=data["check_out"],
                check_out__gt=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those datas are already taken."
            )
        return data
