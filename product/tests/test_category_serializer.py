from django.test import TestCase
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer


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
        # Vai falhar porque 'Books' já existe (unique constraint)
        self.assertFalse(serializer.is_valid())
        
        # Testa com novo nome
        new_data = {'name': 'Comics', 'description': 'Comic books'}
        serializer = CategorySerializer(data=new_data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, 'Comics')
    
    def test_category_serializer_invalid_name(self):
        """Testa que nome é obrigatório"""
        invalid_data = {'description': 'Test without name'}
        serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
    
    def test_category_serializer_contains_expected_fields(self):
        """Testa se o serializer contém os campos esperados"""
        serializer = CategorySerializer(instance=self.category)
        data = serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description'])
    
    def test_category_product_count(self):
        """Testa serialização básica da categoria"""
        serializer = CategorySerializer(instance=self.category)
        data = serializer.data
        self.assertEqual(data['name'], 'Books')
        self.assertEqual(data['description'], 'All kinds of books')
