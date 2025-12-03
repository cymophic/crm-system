#!/bin/sh
set -e

# Auto-run migrations in development only
if [ "${ENVIRONMENT}" = "dev" ] || [ "${ENVIRONMENT}" = "development" ]; then
    echo "Running database migrations..."
    uv run python manage.py migrate --noinput
fi

# Collect static files
echo "Collecting static files..."
uv run python manage.py collectstatic --noinput --clear

# Run appropriate server based on environment
if [ "${ENVIRONMENT}" = "dev" ] || [ "${ENVIRONMENT}" = "development" ]; then
    echo "Starting Django development server..."
    exec uv run python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn..."
    exec uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000
fi