from django.contrib import admin
from .models import ChattingRoom


@admin.register(ChattingRoom)
class ChattingRoomAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
        "updated_at"
    )
    list_filter = ("created_at",)

@admin.register(admin.ModelAdmin)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "text",
        "user",
        "chat_room",
        "created_at"
    )
    list_filter = "created_at",
