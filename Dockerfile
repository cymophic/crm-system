# Base image for your application
FROM python:3.13-slim-bookworm

# Environment setup
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install Python dependencies using uv
COPY pyproject.toml uv.lock ./ 

# Use uv sync --locked to install packages based on uv.lock
RUN uv sync --locked

# Copy project code
COPY . .

# Prepare static files for WhiteNoise
RUN python manage.py collectstatic --noinput

# Expose Gunicorn port
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]