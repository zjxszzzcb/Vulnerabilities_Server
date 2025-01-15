from django.urls import path
from . import views

urlpatterns = [
    path("get", views.order_get),
    path("add", views.order_add),
    path("detail", views.order_detail),
    path("delete/<int:id>", views.order_delete),
]