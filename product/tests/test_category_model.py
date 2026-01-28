from django.test import TestCase
from product.models.category import Category
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
    
    def test_category_ordering(self):
        """Testa se as categorias são ordenadas por nome"""
        Category.objects.create(name='Books')
        Category.objects.create(name='Accessories')
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, 'Accessories')
        self.assertEqual(categories[1].name, 'Books')
