from django.contrib import admin
from .models import Bookings

@admin.register(Bookings)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "user",
        "room",
        "experience",
        "check_in",
        "check_out",
        "experience_time",
        "guests",
    )
    list_filter = ("kind",)
