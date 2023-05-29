from django.urls import path
from . import views


urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:pk>", views.RoomsDetail.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmedityDetail.as_view()),
]
