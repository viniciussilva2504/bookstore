from django.test import TestCase
from order.factories import OrderFactory
from order.serializers.order_serializer import OrderSerializer
from product.factories import ProductFactory
from decimal import Decimal


class TestOrderSerializer(TestCase):
    def setUp(self):
        self.product = ProductFactory(title='Pro controller', price=200.00)
        self.order = OrderFactory()
        self.order.product.add(self.product)
        self.order_serializer = OrderSerializer(self.order)

    def test_order_serializer(self):
        serializer_data = self.order_serializer.data
        
        self.assertEqual(serializer_data['product'][0]['title'], self.product.title)
        self.assertEqual(Decimal(serializer_data['product'][0]['price']), Decimal(str(self.product.price)))
        self.assertEqual(Decimal(serializer_data['total']), Decimal(str(self.product.price)))
