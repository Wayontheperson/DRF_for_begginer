from django.urls import path
from . import views


urlpatterns = [
    path("amenities/", views.Amenities.as_view()),
]