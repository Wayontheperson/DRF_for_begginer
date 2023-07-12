from django.urls import path
from .views import Whishlists


urlpatterns =[
    path("",Whishlists.as_view()),
]