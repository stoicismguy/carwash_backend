#!/bin/bash
set -e  # Выход при ошибке
poetry install
# Миграции, если нужны
poetry run python src/manage.py migrate

# Запуск сервера (для разработки)
# exec poetry run python manage.py runserver 0.0.0.0:8000
# Или для продакшена, например:
exec poetry run gunicorn settings.wsgi:application --bind 0.0.0.0:8000