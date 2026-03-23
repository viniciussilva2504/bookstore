# Deploy no PythonAnywhere - Bookstore API

## Pré-requisitos
- Conta no [PythonAnywhere](https://www.pythonanywhere.com/) (free tier funciona)
- Código no GitHub

---

## Passo a Passo

### 1. Abra o Console Bash no PythonAnywhere

No dashboard, clique em **"Consoles"** > **"$ Bash"** (New console).

### 2. Clone o Repositório

```bash
cd ~
git clone https://github.com/SEU_USUARIO/bookstore.git
cd bookstore
```

### 3. Crie o Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.13 bookstore-venv
```

> **Nota:** PythonAnywhere free tier pode não ter Python 3.14 ainda. Use a versão mais recente disponível (3.13 ou 3.12). Verifique com `ls /usr/bin/python3.*`

### 4. Instale as Dependências

```bash
cd ~/bookstore
pip install -r requirements.txt
```

### 5. Configure o Arquivo .env

```bash
cd ~/bookstore
cp .env.production .env
```

Edite o `.env` com seus dados:
```bash
nano .env
```

Preencha:
```
DEBUG=0
SECRET_KEY=gere-uma-chave-aqui
DJANGO_ALLOWED_HOSTS=SEU_USUARIO.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://SEU_USUARIO.pythonanywhere.com
SECURE_SSL_REDIRECT=1
SQL_ENGINE=django.db.backends.sqlite3
SQL_DATABASE=/home/SEU_USUARIO/bookstore/db.sqlite3
```

**Para gerar uma SECRET_KEY segura**, execute no console:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Execute as Migrações e Collectstatic

```bash
cd ~/bookstore
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 7. Configure o Web App

No dashboard do PythonAnywhere:

1. Vá em **"Web"** > **"Add a new web app"**
2. Escolha **"Manual configuration"** (NÃO escolha Django)
3. Selecione a versão do Python (mesma do virtualenv)

### 8. Configure o Virtual Environment

Na página Web, na seção **"Virtualenv"**:
```
/home/SEU_USUARIO/.virtualenvs/bookstore-venv
```

### 9. Configure o WSGI

Clique no link do arquivo WSGI (algo como `/var/www/SEU_USUARIO_pythonanywhere_com_wsgi.py`).

**Apague todo o conteúdo** e substitua por:

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

### 10. Configure os Static Files

Na página Web, na seção **"Static files"**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/SEU_USUARIO/bookstore/staticfiles` |

### 11. Recarregue o Web App

Clique no botão verde **"Reload"** no topo da página Web.

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
