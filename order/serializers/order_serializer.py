from rest_framework import serializers
from order.models import Order
from product.serializers.product_serializer import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=__import__('product.models.product', fromlist=['Product']).Product.objects.all(),
        write_only=True,
        required=False,
        source='product'
    )
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total

    class Meta:
        model = Order
        fields = ['product', 'product_ids', 'total', 'user']
        extra_kwargs = {
            'product': {'required': False},
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        products_data = validated_data.pop('product', [])
        
        order = Order.objects.create(**validated_data)
        for product in products_data:
            order.product.add(product)
        return order