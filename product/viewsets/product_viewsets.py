from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from product.models import Product
from product.serializers.product_serializer import ProductSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """
        Permite filtrar produtos por título, categoria e faixa de preço
        """
        queryset = Product.objects.all()
        
        # Filtro por título
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        
        # Filtro por categoria
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)
        
        # Filtro por preço mínimo
        min_price = self.request.query_params.get('min_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        # Filtro por preço máximo
        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Retorna produtos em destaque (exemplo: mais caros)
        """
        products = Product.objects.all().order_by('-price')[:5]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Busca avançada por produtos
        """
        query = request.query_params.get('q', '')
        if query:
            products = Product.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        else:
            products = Product.objects.all()
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)