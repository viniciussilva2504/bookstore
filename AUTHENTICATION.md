# Autenticação via Token - Bookstore API

## Visão Geral

O projeto agora possui autenticação via token implementada usando Django REST Framework Token Authentication. Todos os endpoints de `product`, `category` e `order` requerem autenticação.

## Endpoints de Autenticação

### 1. Login (Obter Token)

**Endpoint:** `POST /api/login/`

**Body:**
```json
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

**Resposta de Sucesso (200):**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "seu_usuario",
    "email": "email@example.com"
}
```

**Respostas de Erro:**
- 400: Credenciais não fornecidas
- 401: Credenciais inválidas

### 2. Logout (Remover Token)

**Endpoint:** `POST /api/logout/`

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Resposta de Sucesso (200):**
```json
{
    "message": "Logout realizado com sucesso"
}
```

### 3. Endpoint Alternativo (DRF Padrão)

**Endpoint:** `POST /api-token-auth/`

Este é o endpoint padrão do Django REST Framework. Retorna apenas o token.

**Body:**
```json
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

**Resposta:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

## Como Usar os Endpoints Protegidos

Todos os endpoints de `product`, `category` e `order` agora requerem autenticação. Você deve incluir o token no header de cada requisição:

**Header:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Exemplos com cURL

**Login:**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Acessar produtos (com autenticação):**
```bash
curl http://localhost:8000/product/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Criar um produto:**
```bash
curl -X POST http://localhost:8000/product/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{"title": "Novo Livro", "price": 29.99, "category": 1}'
```

**Logout:**
```bash
curl -X POST http://localhost:8000/api/logout/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Exemplos com Python Requests

```python
import requests

# Login
response = requests.post(
    'http://localhost:8000/api/login/',
    json={'username': 'admin', 'password': 'admin123'}
)
token = response.json()['token']

# Usar o token para acessar recursos protegidos
headers = {'Authorization': f'Token {token}'}

# Listar produtos
products = requests.get('http://localhost:8000/product/', headers=headers)
print(products.json())

# Criar um produto
new_product = requests.post(
    'http://localhost:8000/product/',
    headers=headers,
    json={'title': 'Novo Livro', 'price': 29.99, 'category': 1}
)

# Logout
logout = requests.post('http://localhost:8000/api/logout/', headers=headers)
```

## Criar um Usuário para Testes

Execute os seguintes comandos para criar um superusuário:

```bash
poetry run python manage.py createsuperuser
```

Ou crie um usuário programaticamente:

```bash
poetry run python manage.py shell
```

```python
from django.contrib.auth.models import User
user = User.objects.create_user('testuser', 'test@example.com', 'testpassword123')
```

## Configuração de Autenticação

O projeto está configurado para aceitar três tipos de autenticação:

1. **Token Authentication** - Recomendado para APIs
2. **Session Authentication** - Útil para desenvolvimento e Django Admin
3. **Basic Authentication** - Para testes simples

A configuração está em `bookstore/settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}
```

## Testando no Postman ou Insomnia

1. Faça login no endpoint `/api/login/`
2. Copie o token retornado
3. Em todas as outras requisições, adicione o header:
   - **Key:** `Authorization`
   - **Value:** `Token SEU_TOKEN_AQUI`

## Segurança

- **Nunca** compartilhe seu token em repositórios públicos
- Tokens são gerados automaticamente no primeiro login
- Use HTTPS em produção
- Tokens não expiram por padrão (considere implementar expiração para produção)
- O logout remove o token do banco de dados, invalidando-o

## Endpoints Protegidos

Todos os seguintes endpoints requerem autenticação via token:

- `GET /product/` - Listar produtos
- `POST /product/` - Criar produto
- `GET /product/{id}/` - Detalhe do produto
- `PUT /product/{id}/` - Atualizar produto
- `DELETE /product/{id}/` - Deletar produto
- `GET /category/` - Listar categorias
- `POST /category/` - Criar categoria
- `GET /category/{id}/` - Detalhe da categoria
- `PUT /category/{id}/` - Atualizar categoria
- `DELETE /category/{id}/` - Deletar categoria
- `GET /order/` - Listar pedidos
- `POST /order/` - Criar pedido
- `GET /order/{id}/` - Detalhe do pedido
- `PUT /order/{id}/` - Atualizar pedido
- `DELETE /order/{id}/` - Deletar pedido
