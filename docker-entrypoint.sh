#!/bin/bash
set -e  # Выход при ошибке

# Миграции, если нужны
poetry run python manage.py migrate

# Запуск сервера (для разработки)
# exec poetry run python manage.py runserver 0.0.0.0:8000
# Или для продакшена, например:
exec poetry run gunicorn carwash.wsgi:application --bind 0.0.0.0:8000