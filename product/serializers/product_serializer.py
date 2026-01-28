from rest_framework import serializers
from product.models.product import Product
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Category.objects.all(),
        write_only=True,
        required=False,
        source='category'
    )

    class Meta:
        model = Product
        fields = [
            'id', 
            'title', 
            'description', 
            'price', 
            'active', 
            'category',
            'category_ids',
            ]

    def create(self, validated_data):
        category_data = validated_data.pop('category', [])

        product = Product.objects.create(**validated_data)
        for category in category_data:
            product.category.add(category)  

        return product