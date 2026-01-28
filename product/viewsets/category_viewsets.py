from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """
        Permite filtrar categorias por nome
        """
        queryset = Category.objects.all()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
