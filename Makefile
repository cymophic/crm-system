ENVIRONMENT = $(shell docker-compose ps --services --filter "status=running" | grep -E "^(dev|prod)$$" | head -1)
MAKEFLAGS += --no-print-directory

.PHONY: setup-dev dev dev-build prod prod-build build status down restart bash reset shell collectstatic superuser migrate migrations showmigrations check test service-logs app-logs error-logs django-logs

# ------------------------------------
# Setup Commands
# ------------------------------------

# Initial setup for development
setup-dev:
	@echo Setting up containers...
	@docker-compose up -d --build
	@uv run python -c "print()"
	@$(MAKE) migrate
	@uv run python -c "print()"
	@$(MAKE) superuser
	@echo Development setup complete!
	@uv run python -c "print()"
	@$(MAKE) service-logs


# ------------------------------------
# Development
# ------------------------------------

# Start development environment
dev:
	@echo Starting development environment...
	@docker-compose --profile dev up -d

# Build image before starting dev environment 
dev-build:
	@echo Building and starting development environment...
	@docker-compose --profile dev up -d --build


# ------------------------------------
# Production
# ------------------------------------

# Run application with production setup
prod:
	@echo Starting production environment...
	@docker-compose --profile prod up -d

# Build image before running production setup
prod-build:
	@echo Building and starting production environment...
	@docker-compose --profile prod up -d --build


# ------------------------------------
# Container Management
# ------------------------------------

# Build or updates images
build:
	@echo Building Docker images...
	@docker-compose build

# Display running containers
status:
	@echo Checking container status...
	@docker-compose ps --format "table {{.Service}}\t{{.Name}}\t{{.Status}}"

# Restart containers
restart:
	@echo Restarting containers...
	@docker-compose restart

# Stop and remove containers (preserves data)
down:
	@echo Stopping and removing containers...
	@docker-compose --profile dev --profile prod down

# Container CLI access
bash:
	@echo Opening container bash shell...
	@docker-compose exec $(ENVIRONMENT) bash

# Removes everything (WARNING: deletes data)
reset:
	@echo Removing ALL containers and volumes...
	@docker-compose down -v
	@echo Removing SQLite database...
	@uv run python -c "import os; os.remove('db.sqlite3') if os.path.exists('db.sqlite3') else None"
	@echo Removing logs folder...
	@uv run python -c "import shutil, os; shutil.rmtree('logs') if os.path.exists('logs') else None"
	@echo Removing media folder...
	@uv run python -c "import shutil, os; shutil.rmtree('media') if os.path.exists('media') else None"
	@echo Removing staticfiles folder...
	@uv run python -c "import shutil, os; shutil.rmtree('staticfiles') if os.path.exists('staticfiles') else None"
	@echo Reset complete...

# ------------------------------------
# Application Management
# ------------------------------------

# Django shell CLI
shell:
	@echo Opening Django shell...
	@docker-compose exec $(ENVIRONMENT) uv run python manage.py shell

# Collect static files for deployment
collectstatic:
	@echo Collecting static files...
	@docker-compose exec $(ENVIRONMENT) uv run python manage.py collectstatic --noinput

# Create a Django superuser account
superuser:
	@echo Creating Django superuser...
	@docker-compose exec $(ENVIRONMENT) uv run python manage.py createsuperuser

# Apply database migrations to the database
migrate:
	@echo Running database migrations...
	@docker-compose exec $(ENVIRONMENT) uv run python manage.py migrate

# Create new Django database migrations
migrations:
	@echo Creating new migrations...
	@docker-compose exec $(ENVIRONMENT) uv run python manage.py makemigrations

# Show pending migrations
showmigrations:
	@echo Showing migration status...
	@docker-compose exec $(ENVIRONMENT) uv run python manage.py showmigrations

# Check for project issues
check:
	@echo Checking for project issues...
	@docker-compose exec $(ENVIRONMENT) uv run python manage.py check

# Run the project test suite
test:
	@echo Running test suite...
	@docker-compose exec $(ENVIRONMENT) uv run python manage.py test

# ------------------------------------
# Log Management
# ------------------------------------

# Display all services output logs
service-logs:
	@uv run python -c "print('Streaming service logs (Ctrl+C to exit)...')"
	-@docker-compose logs -f

# View application logs (from logs/app.log)
app-logs:
	@uv run python -c "print('Streaming application logs (Ctrl+C to exit)...')"
	@docker-compose exec $(ENVIRONMENT) tail -f logs/app.log

# View error logs (from logs/errors.log)
error-logs:
	@uv run python -c "print('Streaming error logs (Ctrl+C to exit)...')"
	@docker-compose exec $(ENVIRONMENT) tail -f logs/errors.log

# View Django logs (from logs/django.log)
django-logs:
	@uv run python -c "print('Streaming Django logs (Ctrl+C to exit)...')"
	@docker-compose exec $(ENVIRONMENT) tail -f logs/django.log