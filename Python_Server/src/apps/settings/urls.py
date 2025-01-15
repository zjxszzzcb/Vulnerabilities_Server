from django.urls import path
from . import views

urlpatterns = [
    path("ping", views.settings_ping),
    path("getdb", views.settings_getdb),
    path("backupsdb", views.settings_backupsdb),
    path("deletedb", views.settings_deletedb),
    path("downdb", views.settings_downdb),
]