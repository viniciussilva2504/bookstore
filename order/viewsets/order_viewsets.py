from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Retorna apenas os pedidos do usuário autenticado
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """
        Endpoint customizado para listar pedidos do usuário
        """
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """
        Automaticamente associa o pedido ao usuário autenticado
        """
        serializer.save(user=self.request.user)
