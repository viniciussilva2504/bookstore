from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from product.models import Product, Category
from product.factories import ProductFactory


class TestProductViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Criar usuário
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Criar categoria
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic products'
        )
        
        # Criar produtos
        self.product1 = ProductFactory(
            title='Laptop',
            price=1500.00,
            description='High-end laptop',
            category=self.category
        )
        self.product2 = ProductFactory(
            title='Mouse',
            price=50.00,
            description='Wireless mouse',
            category=self.category
        )
        self.product3 = ProductFactory(
            title='Keyboard',
            price=150.00,
            description='Mechanical keyboard'
        )

    def test_list_products_without_authentication(self):
        """Testa que listagem de produtos não requer autenticação"""
        response = self.client.get('/product/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_product_requires_authentication(self):
        """Testa que criação de produto requer autenticação"""
        data = {
            'title': 'New Product',
            'price': 100.00
        }
        response = self.client.post('/product/', data, format='json')
        # IsAuthenticatedOrReadOnly retorna 403 ao tentar escrever sem auth
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_with_authentication(self):
        """Testa criação de produto com autenticação"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'New Product',
            'price': 100.00,
            'description': 'A new product'
        }
        response = self.client.post('/product/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Product')

    def test_filter_products_by_title(self):
        """Testa filtro de produtos por título"""
        response = self.client.get('/product/?title=Laptop')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Laptop')

    def test_filter_products_by_category(self):
        """Testa filtro de produtos por categoria"""
        response = self.client.get(f'/product/?category={self.category.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_products_by_min_price(self):
        """Testa filtro de produtos por preço mínimo"""
        response = self.client.get('/product/?min_price=100')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for product in response.data:
            self.assertGreaterEqual(float(product['price']), 100.00)

    def test_filter_products_by_max_price(self):
        """Testa filtro de produtos por preço máximo"""
        response = self.client.get('/product/?max_price=200')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for product in response.data:
            self.assertLessEqual(float(product['price']), 200.00)

    def test_filter_products_by_price_range(self):
        """Testa filtro de produtos por faixa de preço"""
        response = self.client.get('/product/?min_price=100&max_price=200')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Keyboard')

    def test_featured_products_endpoint(self):
        """Testa endpoint de produtos em destaque"""
        response = self.client.get('/product/featured/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica que retorna até 5 produtos ordenados por preço
        self.assertLessEqual(len(response.data), 5)
        if len(response.data) > 1:
            # Verifica ordenação decrescente por preço
            prices = [float(p['price']) for p in response.data]
            self.assertEqual(prices, sorted(prices, reverse=True))

    def test_search_endpoint(self):
        """Testa endpoint de busca"""
        response = self.client.get('/product/search/?q=laptop')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_search_endpoint_empty_query(self):
        """Testa endpoint de busca com query vazia"""
        response = self.client.get('/product/search/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_product(self):
        """Testa recuperação de produto específico"""
        response = self.client.get(f'/product/{self.product1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Laptop')

    def test_update_product_requires_authentication(self):
        """Testa que atualização requer autenticação"""
        data = {'title': 'Updated Laptop'}
        response = self.client.patch(f'/product/{self.product1.id}/', data, format='json')
        # IsAuthenticatedOrReadOnly retorna 403 ao tentar escrever sem auth
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_with_authentication(self):
        """Testa atualização de produto com autenticação"""
        self.client.force_authenticate(user=self.user)
        
        data = {'title': 'Updated Laptop'}
        response = self.client.patch(f'/product/{self.product1.id}/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Laptop')

    def test_delete_product_requires_authentication(self):
        """Testa que deleção requer autenticação"""
        response = self.client.delete(f'/product/{self.product1.id}/')
        # IsAuthenticatedOrReadOnly retorna 403 ao tentar escrever sem auth
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_with_authentication(self):
        """Testa deleção de produto com autenticação"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/product/{self.product3.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verifica que o produto foi deletado
        self.assertFalse(Product.objects.filter(id=self.product3.id).exists())
