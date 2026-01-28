from django.test import TestCase
from django.contrib.auth.models import User
from order.models import Order
from product.models import Product


class OrderModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.product = Product.objects.create(
            title='Test Product',
            price=10.00
        )
        
        self.order = Order.objects.create(user=self.user)
        self.order.product.add(self.product)

    def test_order_creation(self):
        """Test that an order can be created"""
        self.assertIsInstance(self.order, Order)
        self.assertEqual(self.order.user, self.user)

    def test_order_product_relationship(self):
        """Test many-to-many relationship with products"""
        self.assertIn(self.product, self.order.product.all())
        self.assertEqual(self.order.product.count(), 1)

    def test_order_user_relationship(self):
        """Test foreign key relationship with user"""
        self.assertEqual(self.order.user.username, 'testuser')
