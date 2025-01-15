from django.urls import path
from . import views

urlpatterns = [
    path("get", views.home_get),
    path("updateInfo", views.home_updateInfo),
    path("updatePwd", views.home_updatePwd),
    path("upuseravatar", views.home_upuseravatar),
    path("getsentence", views.home_getsentence),
]