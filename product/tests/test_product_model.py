from django.test import TestCase
from product.models.category import Category
from product.models.product import Product
from decimal import Decimal


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
    
    def test_product_multiple_categories(self):
        """Testa produto com múltiplas categorias"""
        category2 = Category.objects.create(name='Computers')
        self.product.category.add(category2)
        self.assertEqual(self.product.category.count(), 2)
    
    def test_product_default_active(self):
        """Testa se o produto é ativo por padrão"""
        product = Product.objects.create(
            title='Mouse',
            price=Decimal('29.99')
        )
        self.assertTrue(product.active)
