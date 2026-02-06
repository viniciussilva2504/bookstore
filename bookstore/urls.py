"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

import debug_toolbar
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from order.viewsets import OrderViewSet
from product.viewsets import CategoryViewSet, ProductViewSet
from api.views import login, logout

router = routers.DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"order", OrderViewSet, basename="order")

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    re_path("bookstore/(?P<version>(v1|v2))/", include("order.urls")),
    re_path("bookstore/(?P<version>(v1|v2))/", include("product.urls")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("api/login/", login, name="login"),
    path("api/logout/", logout, name="logout"),
]
