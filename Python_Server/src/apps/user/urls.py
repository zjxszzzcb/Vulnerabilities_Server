from django.urls import path
from . import views

urlpatterns = [
    path("get", views.user_get),
    path("add", views.user_add),
    path("detail", views.user_detail),
    path("update", views.user_update),
    path("delete/<int:id>", views.user_delete),
]