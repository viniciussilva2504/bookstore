# Notas do Projeto Bookstore

## Problemas Resolvidos

### 1. Linha amarela em imports (.models, .category, .product)
**Causa:** VS Code não encontrava os arquivos referenciados nos imports relativos.

**Solução:** 
- Criar os arquivos faltantes (`models.py`, `category.py`, `product.py`)
- Recarregar o VS Code se necessário (`Ctrl+Shift+P` > "Reload Window")
- Verificar se o interpretador Python correto está selecionado

### 2. Erro "ModuleNotFoundError: No module named 'rest_framework'"
**Causa:** Pacote `djangorestframework` não estava instalado.

**Solução:**
```bash
poetry add djangorestframework
```

## Dependências Instaladas (poetry.lock)
- Django 6.0.1
- djangorestframework 3.16.1
- factory-boy 3.3.3 (dev)
- Faker 40.1.2 (dev)

## Comandos Úteis

### Ativar ambiente Poetry
```bash
poetry shell
```

### Instalar dependências
```bash
poetry install
```

### Adicionar nova dependência
```bash
poetry add nome-do-pacote
```

### Migrações Django
```bash
python manage.py makemigrations
python manage.py migrate
```

### Executar servidor
```bash
python manage.py runserver
```

## Estrutura do Projeto
```
bookstore/
├── product/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── category.py (se necessário)
│   └── product.py (se necessário)
├── manage.py
├── poetry.lock
└── pyproject.toml
```

## Observações
- Sempre usar Poetry para gerenciar dependências
- Imports relativos (com ponto `.`) são usados dentro de packages Django
- A linha amarela no VS Code geralmente indica arquivo faltante ou configuração do interpretador