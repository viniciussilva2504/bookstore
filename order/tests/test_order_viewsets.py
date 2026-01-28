from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from order.models import Order
from order.factories import OrderFactory
from product.factories import ProductFactory


class TestOrderViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Criar usuários
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True
        )
        
        # Criar produtos
        self.product1 = ProductFactory(title='Product 1', price=100.00)
        self.product2 = ProductFactory(title='Product 2', price=200.00)
        
        # Criar pedidos
        self.order1 = OrderFactory(user=self.user1)
        self.order1.product.add(self.product1)
        
        self.order2 = OrderFactory(user=self.user2)
        self.order2.product.add(self.product2)

    def test_list_orders_requires_authentication(self):
        """Testa que listagem de pedidos requer autenticação"""
        response = self.client.get('/order/')
        # IsAuthenticated retorna 403 quando não autenticado
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_only_see_own_orders(self):
        """Testa que usuário só vê seus próprios pedidos"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/order/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user1.id)

    def test_admin_can_see_all_orders(self):
        """Testa que admin vê todos os pedidos"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/order/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_my_orders_endpoint(self):
        """Testa endpoint customizado my_orders"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/order/my_orders/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_order_auto_assigns_user(self):
        """Testa que criação de pedido associa automaticamente o usuário"""
        self.client.force_authenticate(user=self.user1)
        
        data = {
            'product_ids': [self.product1.id]
        }
        response = self.client.post('/order/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user1.id)

    def test_user_cannot_access_other_user_order(self):
        """Testa que usuário não pode acessar pedido de outro usuário"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/order/{self.order2.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_own_order(self):
        """Testa que usuário pode ver detalhes do próprio pedido"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/order/{self.order1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user1.id)
