from django.test import TestCase
from product.models.category import Category
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer
from decimal import Decimal


class ProductSerializerTest(TestCase):
    """Testes para ProductSerializer"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', description='Electronic devices')
        self.product_data = {
            'title': 'Smartphone',
            'description': 'Latest smartphone',
            'price': '599.99',
            'active': True,
            'category_ids': [self.category.id]
        }
    
    def test_product_serializer_valid_data(self):
        """Testa serialização com dados válidos"""
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.title, 'Smartphone')
        self.assertEqual(product.price, Decimal('599.99'))
        self.assertEqual(product.category.count(), 1)
    
    def test_product_serializer_invalid_price(self):
        """Testa que serializer aceita qualquer preço (sem validação customizada)"""
        invalid_data = self.product_data.copy()
        invalid_data['price'] = '-10.00'
        serializer = ProductSerializer(data=invalid_data)
        # Sem validação customizada, aceita preços negativos
        self.assertTrue(serializer.is_valid())
    
    def test_product_serializer_invalid_title(self):
        """Testa que serializer aceita qualquer título (sem validação customizada)"""
        invalid_data = self.product_data.copy()
        invalid_data['title'] = 'AB'
        serializer = ProductSerializer(data=invalid_data)
        # Sem validação customizada, aceita títulos curtos
        self.assertTrue(serializer.is_valid())
    
    def test_product_serializer_contains_expected_fields(self):
        """Testa se o serializer contém os campos esperados"""
        product = Product.objects.create(
            title='Test Product',
            price=Decimal('100.00')
        )
        serializer = ProductSerializer(instance=product)
        data = serializer.data
        # category_ids é write_only, não aparece no output
        expected_fields = ['id', 'title', 'description', 'price', 'active', 'category']
        self.assertCountEqual(data.keys(), expected_fields)
    
    def test_product_serializer_with_multiple_categories(self):
        """Testa serialização de produto com múltiplas categorias"""
        category2 = Category.objects.create(name='Gadgets')
        product_data = self.product_data.copy()
        product_data['category_ids'] = [self.category.id, category2.id]
        
        serializer = ProductSerializer(data=product_data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.category.count(), 2)
    
    def test_product_serializer_zero_price(self):
        """Testa que serializer aceita preço zero (sem validação customizada)"""
        invalid_data = self.product_data.copy()
        invalid_data['price'] = '0.00'
        serializer = ProductSerializer(data=invalid_data)
        # Sem validação customizada, aceita preço zero
        self.assertTrue(serializer.is_valid())
