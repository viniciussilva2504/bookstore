from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from product.models import Category


class TestCategoryViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Criar usuário
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Criar categorias
        self.category1 = Category.objects.create(
            name='Electronics',
            description='Electronic devices and accessories'
        )
        self.category2 = Category.objects.create(
            name='Books',
            description='Books and magazines'
        )
        self.category3 = Category.objects.create(
            name='Clothing',
            description='Clothes and fashion'
        )

    def test_list_categories_without_authentication(self):
        """Testa que listagem de categorias não requer autenticação"""
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_category_without_authentication(self):
        """Testa que visualização de categoria não requer autenticação"""
        response = self.client.get(f'/category/{self.category1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Electronics')

    def test_create_category_requires_authentication(self):
        """Testa que criação de categoria requer autenticação"""
        data = {
            'name': 'Sports',
            'description': 'Sports equipment'
        }
        response = self.client.post('/category/', data, format='json')
        # IsAuthenticatedOrReadOnly retorna 403 ao tentar escrever sem auth
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_with_authentication(self):
        """Testa criação de categoria com autenticação"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'name': 'Sports',
            'description': 'Sports equipment and accessories'
        }
        response = self.client.post('/category/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Sports')
        self.assertEqual(response.data['description'], 'Sports equipment and accessories')

    def test_filter_categories_by_name(self):
        """Testa filtro de categorias por nome"""
        response = self.client.get('/category/?name=Electronics')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Electronics')

    def test_filter_categories_by_partial_name(self):
        """Testa filtro de categorias por nome parcial (case insensitive)"""
        response = self.client.get('/category/?name=book')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Books')

    def test_update_category_requires_authentication(self):
        """Testa que atualização requer autenticação"""
        data = {'name': 'Updated Electronics'}
        response = self.client.patch(
            f'/category/{self.category1.id}/',
            data,
            format='json'
        )
        # IsAuthenticatedOrReadOnly retorna 403 ao tentar escrever sem auth
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_with_authentication(self):
        """Testa atualização de categoria com autenticação"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'name': 'Updated Electronics',
            'description': 'Updated description'
        }
        response = self.client.patch(
            f'/category/{self.category1.id}/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Electronics')
        self.assertEqual(response.data['description'], 'Updated description')

    def test_delete_category_requires_authentication(self):
        """Testa que deleção requer autenticação"""
        response = self.client.delete(f'/category/{self.category1.id}/')
        # IsAuthenticatedOrReadOnly retorna 403 ao tentar escrever sem auth
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_with_authentication(self):
        """Testa deleção de categoria com autenticação"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/category/{self.category3.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verifica que a categoria foi deletada
        self.assertFalse(Category.objects.filter(id=self.category3.id).exists())

    def test_category_name_is_required(self):
        """Testa que o nome da categoria é obrigatório"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'description': 'Category without name'
        }
        response = self.client.post('/category/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verifica que há erro relacionado a campos obrigatórios
        self.assertTrue('name' in response.data or 'non_field_errors' in response.data)

    def test_get_all_categories_returns_correct_structure(self):
        """Testa que a listagem retorna a estrutura correta"""
        response = self.client.get('/category/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica estrutura do primeiro item
        first_category = response.data[0]
        self.assertIn('id', first_category)
        self.assertIn('name', first_category)
        self.assertIn('description', first_category)

    def test_full_update_category(self):
        """Testa atualização completa de categoria com PUT"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'name': 'Completely New Name',
            'description': 'Completely new description'
        }
        response = self.client.put(
            f'/category/{self.category1.id}/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Completely New Name')
        self.assertEqual(response.data['description'], 'Completely new description')
