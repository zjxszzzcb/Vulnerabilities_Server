from django.urls import path
from . import views

urlpatterns = [
    path("get", views.food_get),
    path("add", views.food_add),
    path("detail", views.food_detail),
    path("update", views.food_update),
    path("delete/<int:id>", views.food_delete),
    path("upfoodicon", views.food_upfoodicon),
    path("upfoodvideo", views.food_upfoodvideo),
]