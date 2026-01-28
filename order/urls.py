from django.urls import path, include
from rest_framework import routers

from order.viewsets import order_viewsets

router = routers.SimpleRouter()
router.register(r'', order_viewsets.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
