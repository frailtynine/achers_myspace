.PHONY: help install migrate run superuser shell test clean collectstatic makemigrations check format lint sync startapp

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies with uv"
	@echo "  make sync           - Sync dependencies from lock file"
	@echo "  make migrate        - Run database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make startapp       - Create a new Django app (usage: make startapp name=appname)"
	@echo "  make run            - Run development server"
	@echo "  make superuser      - Create a superuser"
	@echo "  make shell          - Start Django shell"
	@echo "  make test           - Run tests"
	@echo "  make check          - Check for project issues"
	@echo "  make collectstatic  - Collect static files"
	@echo "  make clean          - Remove Python cache files"
	@echo "  make format         - Format code with black"
	@echo "  make lint           - Lint code with flake8"

install:
	uv sync

sync:
	uv sync

migrate:
	cd achers_myspace && uv run python manage.py migrate

makemigrations:
	cd achers_myspace && uv run python manage.py makemigrations

startapp:
	@test -n "$(name)" || (echo "Error: Please specify app name with name=appname" && exit 1)
	cd achers_myspace && uv run python manage.py startapp $(name)

run:
	cd achers_myspace && uv run python manage.py runserver

superuser:
	cd achers_myspace && uv run python manage.py createsuperuser

shell:
	cd achers_myspace && uv run python manage.py shell

test:
	cd achers_myspace && uv run python manage.py test

check:
	cd achers_myspace && uv run python manage.py check

collectstatic:
	cd achers_myspace && uv run python manage.py collectstatic --noinput

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete

format:
	@command -v black >/dev/null 2>&1 && black . || echo "black not installed. Run: pip install black"

lint:
	@command -v flake8 >/dev/null 2>&1 && flake8 . || echo "flake8 not installed. Run: pip install flake8"
