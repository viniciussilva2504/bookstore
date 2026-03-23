# Deploy no PythonAnywhere - Bookstore API

## Pré-requisitos
- Conta no [PythonAnywhere](https://www.pythonanywhere.com/) (free tier funciona)
- Código no GitHub: https://github.com/viniciussilva2504/bookstore.git

---

## Passo a Passo

### 1. Crie sua conta no PythonAnywhere

1. Acesse **https://www.pythonanywhere.com/**
2. Clique em **"Pricing & signup"**
3. Escolha **"Create a Beginner account"** (gratuito)
4. Preencha seus dados e confirme o email
> **IMPORTANTE:** Anote seu username, ele será parte da sua URL final.

### 2. Abra o Console Bash

No dashboard, clique em **"Consoles"** > na seção "Other" clique em **"Bash"**.

### 3. Clone o Repositório

```bash
cd ~
git clone -b producao https://github.com/viniciussilva2504/bookstore.git
cd bookstore
```

### 4. Crie o Virtual Environment

Primeiro, veja qual versão do Python está disponível:
```bash
ls /usr/bin/python3.*
```

Depois crie o virtualenv (use a versão mais recente disponível):
```bash
mkvirtualenv --python=/usr/bin/python3.10 bookstore-venv
```
> Se tiver 3.12 ou 3.13 disponível, use essa versão no lugar de 3.10.

### 5. Instale as Dependências

```bash
cd ~/bookstore
pip install -r requirements.txt
```

### 6. Configure o Arquivo .env

```bash
cd ~/bookstore
cp .env.production .env
```

Gere uma SECRET_KEY segura:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie a chave gerada e edite o `.env`:
```bash
nano .env
```

Substitua `SEU_USUARIO` pelo seu username do PythonAnywhere e cole a SECRET_KEY:
```
DEBUG=0
SECRET_KEY=COLE_A_CHAVE_GERADA_AQUI
DJANGO_ALLOWED_HOSTS=SEU_USUARIO.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://SEU_USUARIO.pythonanywhere.com
SECURE_SSL_REDIRECT=1
SQL_ENGINE=django.db.backends.sqlite3
SQL_DATABASE=/home/SEU_USUARIO/bookstore/db.sqlite3
```

Salve com **Ctrl+O**, Enter, e saia com **Ctrl+X**.

### 7. Execute as Migrações

```bash
cd ~/bookstore
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```
> No `createsuperuser`, defina username, email e senha para acessar o admin.

### 8. Configure o Web App

1. No dashboard, vá em **"Web"** (menu superior)
2. Clique em **"Add a new web app"**
3. Clique **"Next"** (aceite o domínio gratuito)
4. Escolha **"Manual configuration"** (NÃO escolha "Django")
5. Selecione a **mesma versão do Python** usada no virtualenv
6. Clique **"Next"** para finalizar

### 9. Configure o Virtual Environment

Na página **Web**, role até a seção **"Virtualenv"** e digite:
```
/home/SEU_USUARIO/.virtualenvs/bookstore-venv
```
Pressione Enter para confirmar.

### 10. Configure o WSGI

Na página **Web**, clique no link do arquivo WSGI (em vermelho, algo como):
```
/var/www/SEU_USUARIO_pythonanywhere_com_wsgi.py
```

**Apague TODO o conteúdo** e cole exatamente isto (trocando SEU_USUARIO):

```python
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Caminho do projeto
project_home = '/home/SEU_USUARIO/bookstore'

# Carrega variáveis de ambiente do .env
env_path = Path(project_home) / '.env'
load_dotenv(env_path)

# Adiciona o projeto ao PATH
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bookstore.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Clique **"Save"** no canto superior direito.

### 11. Configure os Static Files

Na página **Web**, role até **"Static files"** e adicione:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/SEU_USUARIO/bookstore/staticfiles` |

### 12. Recarregue e Teste

1. Role até o topo da página **Web**
2. Clique no botão verde **"Reload SEU_USUARIO.pythonanywhere.com"**
3. Acesse: **https://SEU_USUARIO.pythonanywhere.com/bookstore/v1/product/**
4. Admin: **https://SEU_USUARIO.pythonanywhere.com/admin/**

### 12. Teste

Acesse: `https://SEU_USUARIO.pythonanywhere.com/bookstore/v1/product/`

---

## Atualizações Futuras

Sempre que fizer alterações no código:

```bash
cd ~/bookstore
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Depois clique em **"Reload"** na página Web do PythonAnywhere.

---

## Usando MySQL (Opcional - Free Tier)

Se preferir MySQL em vez de SQLite:

1. No dashboard, vá em **"Databases"**
2. Crie o banco e defina a senha
3. Instale o driver: `pip install mysqlclient`
4. Atualize o `.env`:

```
SQL_ENGINE=django.db.backends.mysql
SQL_DATABASE=SEU_USUARIO$bookstore
SQL_USER=SEU_USUARIO
SQL_PASSWORD=SUA_SENHA_MYSQL
SQL_HOST=SEU_USUARIO.mysql.pythonanywhere-services.com
SQL_PORT=3306
```

5. Execute: `python manage.py migrate`
6. Reload o web app

---

## Troubleshooting

- **500 Internal Server Error**: Verifique o error log em Web > Log files > Error log
- **Static files não carregam**: Confirme o caminho em Static files e rode `collectstatic`
- **ModuleNotFoundError**: Confirme que o virtualenv está configurado corretamente
- **DisallowedHost**: Adicione o domínio em `DJANGO_ALLOWED_HOSTS` no `.env`
