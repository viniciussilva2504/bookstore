# 📚 Bookstore API

REST API for bookstore management, built with **Django 6** and **Django REST Framework**.

https://vjsilva250490.pythonanywhere.com/bookstore/v1/product/

## Technologies

- **Python** 3.14
- **Django** 6.0
- **Django REST Framework** 3.16
- **PostgreSQL** 15
- **Docker** & **Docker Compose**
- **Poetry** 2.1 (dependency management)

## Features

- **Products** CRUD (`/bookstore/v1/product/`)
- **Categories** CRUD (`/bookstore/v1/category/`)
- **Orders** CRUD (`/bookstore/v1/order/`)
- API versioning (`v1`, `v2`)
- Token authentication (`/api-token-auth/`)
- Django admin panel (`/admin/`)

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- Or [Python 3.14+](https://www.python.org/) with [Poetry](https://python-poetry.org/)

## Quick Start (Docker)

```bash
# Start services (API + PostgreSQL)
docker-compose up --build

# The API will be available at http://localhost:8000
```

## Quick Start (Local)

```bash
# Install dependencies
poetry install

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

## Useful Commands (Makefile)

| Command            | Description                      |
| ------------------ | -------------------------------- |
| `make build`       | Build Docker image               |
| `make run`         | Run container in detached mode   |
| `make stop`        | Stop container                   |
| `make shell`       | Access container shell           |
| `make test`        | Run tests                        |
| `make migrations`  | Create Django migrations         |
| `make migrate`     | Apply Django migrations          |
| `make clean`       | Remove container and image       |
| `make lint`        | Run linting (flake8)             |
| `make format-py`   | Format code (black)              |

## Project Structure

```
bookstore/
├── bookstore/          # Django project settings
├── api/                # Base API app
├── product/            # Products and Categories app
│   ├── models/
│   ├── serializers/
│   ├── viewsets/
│   └── tests/
├── order/              # Orders app
│   ├── models/
│   ├── serializers/
│   ├── viewsets/
│   └── tests/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Tests

```bash
# Via Docker
make test

# Locally
python manage.py test
```

## Environment Variables

Variables are defined in the `env.dev` file. Main ones:

| Variable            | Description              |
| ------------------- | ------------------------ |
| `SECRET_KEY`        | Django secret key        |
| `DEBUG`             | Debug mode (0 or 1)     |
| `POSTGRES_USER`     | PostgreSQL user          |
| `POSTGRES_PASSWORD` | PostgreSQL password      |
| `POSTGRES_DB`       | Database name            |

## License

This project is for educational purposes only.
