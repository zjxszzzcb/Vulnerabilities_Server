from django.urls import path
from . import views

urlpatterns = [
    path("uploadzip", views.other_uploadzip),
]