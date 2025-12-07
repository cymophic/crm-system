MAKEFLAGS += --no-print-directory
-include .env
export ENVIRONMENT ?= dev

.PHONY: setup-dev dev dev-build prod prod-build build status down restart bash clean reset shell collectstatic superuser migrate migrations showmigrations check test tailwind-build manage.py service-logs app-logs error-logs django-logs

# ------------------------------------
# Setup Commands
# ------------------------------------

# Initial setup for development
setup-dev:
	@echo Setting up dev containers...
	@docker-compose --profile dev up -d --build
	@uv run python -c "print()"
	@$(MAKE) migrate
	@uv run python -c "print()"
	@$(MAKE) restart
	@uv run python -c "print()"
	@$(MAKE) superuser
	@uv run python -c "print()"
	@$(MAKE) service-logs lines=13
	@uv run python -c "print()"
	@echo Development environment setup complete!


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
	@docker-compose --profile $(ENVIRONMENT) build

# Display running containers
status:
	@echo Checking container status...
	@docker-compose ps --format "table {{.ID}}\t{{.Service}}\t{{.Name}}\t{{.Status}}"

# Restart containers
restart:
	@echo Restarting containers...
	@docker-compose --profile $(ENVIRONMENT) restart

# Stop and remove containers (preserves data)
down:
	@echo Stopping and removing containers...
	@docker-compose --profile $(ENVIRONMENT) down

# Container CLI access
bash:
	@echo Opening container bash shell...
	@docker-compose exec $(ENVIRONMENT) bash

# Remove generated files and caches (keeps containers)
clean:
	@echo Removing Python cache files...
	@uv run python -c "import os, shutil, glob; [shutil.rmtree(d) for d in glob.glob('**/__pycache__', recursive=True) if os.path.isdir(d)]"
	@echo Removing .pyc files...
	@uv run python -c "import os, glob; [os.remove(f) for f in glob.glob('**/*.pyc', recursive=True) if os.path.isfile(f)]"
	@echo Removing pytest cache...
	@uv run python -c "import shutil; shutil.rmtree('.pytest_cache', ignore_errors=True)"
	@echo Removing .egg-info directories...
	@uv run python -c "import os, shutil, glob; [shutil.rmtree(d) for d in glob.glob('**/*.egg-info', recursive=True) if os.path.isdir(d)]"
	@echo Removing macOS Finder files...
	@uv run python -c "import os, glob; [os.remove(f) for f in glob.glob('**/.DS_Store', recursive=True) if os.path.isfile(f)]"
	@echo Removing Thumbs.db files...
	@uv run python -c "import os, glob; [os.remove(f) for f in glob.glob('**/Thumbs.db', recursive=True) if os.path.isfile(f)]"
	@echo Clean complete!

# Removes everything (WARNING: deletes data)
reset:
	@echo Removing ALL containers and volumes...
	@docker-compose --profile dev --profile prod down -v
	@echo Removing SQLite database...
	@uv run python -c "import os; os.remove('db.sqlite3') if os.path.exists('db.sqlite3') else None"
	@echo Removing logs folder...
	@uv run python -c "import shutil, os; shutil.rmtree('logs') if os.path.exists('logs') else None"
	@echo Removing media folder...
	@uv run python -c "import shutil, os; shutil.rmtree('media') if os.path.exists('media') else None"
	@echo Removing staticfiles folder...
	@uv run python -c "import shutil, os; shutil.rmtree('staticfiles') if os.path.exists('staticfiles') else None"
	@echo Reset complete!

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

# Build minified CSS for production
tailwind-build:
	@echo Building Tailwind CSS...
	@docker-compose exec $(ENVIRONMENT) uv run python manage.py tailwind build --force

# Run custom manage.py command
manage.py:
	@docker-compose exec $(ENVIRONMENT) uv run python manage.py $(cmd)

# ------------------------------------
# Log Management
# ------------------------------------

# Display all services output logs
service-logs:
	@echo Showing last $(or $(lines),20) lines of service logs...
	@docker-compose logs $(ENVIRONMENT) --tail=$(or $(lines),20)

# View application logs (from logs/app.log)
app-logs:
	@echo Showing last $(or $(lines),20) lines of application logs...
	@docker-compose exec $(ENVIRONMENT) tail -n $(or $(lines),20) logs/app.log

# View error logs (from logs/errors.log)
error-logs:
	@echo Showing last $(or $(lines),20) lines of error logs...
	@docker-compose exec $(ENVIRONMENT) tail -n $(or $(lines),20) logs/errors.log

# View Django logs (from logs/django.log)
django-logs:
	@echo Showing last $(or $(lines),20) lines of Django logs...
	@docker-compose exec $(ENVIRONMENT) tail -n $(or $(lines),20) logs/django.log