from rest_framework import serializers

from product.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Category.
    Gerencia a serialização e validação de categorias de produtos.
    """
    class Meta:
        model = Category
        fields = [
            "title",
            "slug",
            "description",
            "active",
        ]
        extra_kwargs = {"slug": {"required": False}}
