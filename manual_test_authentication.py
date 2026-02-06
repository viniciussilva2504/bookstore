"""
Script de teste para validar a autenticação via token
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_login():
    """Testa o endpoint de login"""
    print("=" * 50)
    print("Testando Login...")
    print("=" * 50)
    
    response = requests.post(
        f'{BASE_URL}/api/login/',
        json={'username': 'testuser', 'password': 'testpass123'}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()['token']
    return None


def test_list_products(token):
    """Testa listagem de produtos com autenticação"""
    print("\n" + "=" * 50)
    print("Testando Listagem de Produtos (com token)...")
    print("=" * 50)
    
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{BASE_URL}/product/', headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_list_products_without_auth():
    """Testa listagem de produtos sem autenticação (deve falhar)"""
    print("\n" + "=" * 50)
    print("Testando Listagem de Produtos (sem token - deve falhar)...")
    print("=" * 50)
    
    response = requests.get(f'{BASE_URL}/product/')
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_logout(token):
    """Testa o endpoint de logout"""
    print("\n" + "=" * 50)
    print("Testando Logout...")
    print("=" * 50)
    
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(f'{BASE_URL}/api/logout/', headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == '__main__':
    print("\n🔐 Iniciando testes de autenticação via token\n")
    
    try:
        # Teste 1: Login
        token = test_login()
        
        if not token:
            print("\n❌ Falha no login. Verifique as credenciais.")
            exit(1)
        
        print(f"\n✅ Token obtido: {token}")
        
        # Teste 2: Listar produtos sem autenticação (deve falhar)
        test_list_products_without_auth()
        
        # Teste 3: Listar produtos com autenticação (deve funcionar)
        test_list_products(token)
        
        # Teste 4: Logout
        test_logout(token)
        
        print("\n" + "=" * 50)
        print("✅ Todos os testes concluídos!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar ao servidor.")
        print("   Certifique-se de que o servidor está rodando:")
        print("   poetry run python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
