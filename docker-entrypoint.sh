#!/bin/sh
set -e


# Run appropriate server based on environment
if [ "${ENVIRONMENT}" = "dev" ] || [ "${ENVIRONMENT}" = "development" ]; then
    echo "Starting Django development server..."
    exec uv run python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn..."
    exec uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000
fi