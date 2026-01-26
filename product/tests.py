from django.test import TestCase
from rest_framework.test import APITestCase
from product.models.category import Category
from product.models.product import Product
from product.serializers.category_serializer import CategorySerializer
from product.serializers.product_serializer import ProductSerializer
from decimal import Decimal


class CategoryModelTest(TestCase):
    """Testes para o modelo Category"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices and gadgets'
        )
    
    def test_category_creation(self):
        """Testa se a categoria foi criada corretamente"""
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.description, 'Electronic devices and gadgets')
        self.assertTrue(isinstance(self.category, Category))
    
    def test_category_str(self):
        """Testa o método __str__ da categoria"""
        self.assertEqual(str(self.category), 'Electronics')
    
    def test_category_unique_name(self):
        """Testa se o nome da categoria é único"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='Electronics', description='Another description')


class CategorySerializerTest(TestCase):
    """Testes para CategorySerializer"""
    
    def setUp(self):
        self.category_data = {
            'name': 'Books',
            'description': 'All kinds of books'
        }
        self.category = Category.objects.create(**self.category_data)
    
    def test_category_serializer_valid_data(self):
        """Testa serialização com dados válidos"""
        serializer = CategorySerializer(data=self.category_data)
        self.assertFalse(serializer.is_valid())  # Vai falhar porque 'Books' já existe
        
        # Testa com novo nome
        new_data = {'name': 'Comics', 'description': 'Comic books'}
        serializer = CategorySerializer(data=new_data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, 'Comics')
    
    def test_category_serializer_invalid_name(self):
        """Testa validação de nome muito curto"""
        invalid_data = {'name': 'AB', 'description': 'Test'}
        serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
    
    def test_category_serializer_contains_expected_fields(self):
        """Testa se o serializer contém os campos esperados"""
        serializer = CategorySerializer(instance=self.category)
        data = serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'product_count', 'created_at', 'updated_at'])


class ProductModelTest(TestCase):
    """Testes para o modelo Product"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            title='Laptop',
            description='High performance laptop',
            price=Decimal('999.99'),
            active=True
        )
        self.product.category.add(self.category)
    
    def test_product_creation(self):
        """Testa se o produto foi criado corretamente"""
        self.assertEqual(self.product.title, 'Laptop')
        self.assertEqual(self.product.price, Decimal('999.99'))
        self.assertTrue(self.product.active)
    
    def test_product_str(self):
        """Testa o método __str__ do produto"""
        self.assertEqual(str(self.product), 'Laptop')
    
    def test_product_category_relationship(self):
        """Testa o relacionamento ManyToMany com Category"""
        self.assertEqual(self.product.category.count(), 1)
        self.assertEqual(self.product.category.first().name, 'Electronics')


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
        """Testa validação de preço inválido"""
        invalid_data = self.product_data.copy()
        invalid_data['price'] = '-10.00'
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
    
    def test_product_serializer_invalid_title(self):
        """Testa validação de título muito curto"""
        invalid_data = self.product_data.copy()
        invalid_data['title'] = 'AB'
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_product_serializer_contains_expected_fields(self):
        """Testa se o serializer contém os campos esperados"""
        product = Product.objects.create(
            title='Test Product',
            price=Decimal('100.00')
        )
        serializer = ProductSerializer(instance=product)
        data = serializer.data
        expected_fields = ['id', 'title', 'description', 'price', 'active', 'category', 'created_at', 'updated_at']
        self.assertCountEqual(data.keys(), expected_fields)
