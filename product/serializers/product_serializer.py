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
        fields = ['id', 'title', 'description', 'price', 'active', 'category', 'category_ids', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Product title must be at least 3 characters long.")
        return value