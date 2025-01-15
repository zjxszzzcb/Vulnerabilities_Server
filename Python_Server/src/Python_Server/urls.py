"""
URL configuration for Python_Server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import path, include, re_path

urlpatterns = [
    # 提供前端构建的静态文件
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.FRONTEND_DIST_DIR, 'show_indexes': True}),
    path("auth/", include("apps.authlogin.urls")),
    path("home/", include("apps.home.urls")),
    path("settings/", include("apps.settings.urls")),
    path("role/", include("apps.role.urls")),
    path("user/", include("apps.user.urls")),
    path("food/", include("apps.food.urls")),
    path("order/", include("apps.order.urls")),
    path("other/", include("apps.other.urls")),
]
# 如果有通配符路由，确保放在最后
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)