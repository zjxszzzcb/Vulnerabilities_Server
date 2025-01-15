from django.urls import path
from . import views

urlpatterns = [
    path("get", views.role_get),
    path("add", views.role_add),
    path("detail", views.role_detail),
    path("update", views.role_update),
    path("delete/<int:id>", views.role_delete),
]