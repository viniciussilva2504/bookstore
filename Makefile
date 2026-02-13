.PHONY: build run stop shell test migrations migrate clean lint format help

help:
	@echo "Available commands:"
	@echo "  make build       - Build Docker image"
	@echo "  make run         - Run container in detached mode"
	@echo "  make stop        - Stop running container"
	@echo "  make shell       - Access container shell"
	@echo "  make test        - Run tests"
	@echo "  make migrations  - Create Django migrations"
	@echo "  make migrate     - Apply Django migrations"
	@echo "  make clean       - Remove container and image"
	@echo "  make lint        - Run code linting"
	@echo "  make format      - Format code with black"

build:
	docker build -t bookstore:latest .

run:
	docker run -d -p 8000:8000 --name bookstore bookstore:latest python manage.py runserver 0.0.0.0:8000

stop:
	docker stop bookstore || true
	docker rm bookstore || true

shell:
	docker exec -it bookstore /bin/bash

test:
	docker exec -it bookstore python manage.py test

migrations:
	docker exec -it bookstore python manage.py makemigrations

migrate:
	docker exec -it bookstore python manage.py migrate

clean: stop
	docker rmi bookstore:latest || true

lint:
	poetry run flake8 . || true

format:
	poetry run black . || true
