from django.urls import path
from . import views

urlpatterns = [
    path("login", views.auth_login),
    path("loginout", views.auth_loginout),
]
