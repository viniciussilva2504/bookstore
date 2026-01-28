from django.urls import path, include
from rest_framework import routers

from product.viewsets import product_viewsets, category_viewsets

product_router = routers.SimpleRouter()
product_router.register(r'', product_viewsets.ProductViewSet, basename='product')

category_router = routers.SimpleRouter()
category_router.register(r'', category_viewsets.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(product_router.urls)),
]
