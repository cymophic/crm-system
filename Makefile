.PHONY: setup-dev dev dev-build prod prod-build build status down restart bash reset shell collectstatic superuser migrate migrations showmigrations check test service-logs app-logs error-logs django-logs


# ------------------------------------
# Setup Commands
# ------------------------------------

# Initial setup for development
setup-dev:
	@echo Setting up containers...
	@docker-compose up -d --build
	@$(MAKE) migrate
	@$(MAKE) superuser
	@echo Development setup complete!



# ------------------------------------
# Development
# ------------------------------------

# Start development environment
dev:
	@echo Starting development environment...
	@docker-compose up -d

# Build image before starting dev environment 
dev-build:
	@echo Building and starting development environment...
	@docker-compose up -d --build


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
	@docker-compose down

# Container CLI access
bash:
	@echo Opening container bash shell...
	@docker-compose exec app bash

# Removes everything (WARNING: deletes data)
reset:
	@echo Removing ALL containers and volumes...
	@docker-compose down -v
	@echo Removing SQLite database...
	@uv run python -c "import os; os.remove('db.sqlite3') if os.path.exists('db.sqlite3') else None"
	@echo Reset complete...

# ------------------------------------
# Application Management
# ------------------------------------

# Django shell CLI
shell:
	@echo Opening Django shell...
	@docker-compose exec app uv run python manage.py shell

# Collect static files for deployment
collectstatic:
	@echo Collecting static files...
	@docker-compose exec app uv run python manage.py collectstatic --noinput

# Create a Django superuser account
superuser:
	@echo Creating Django superuser...
	@docker-compose exec app uv run python manage.py createsuperuser

# Apply database migrations to the database
migrate:
	@echo Running database migrations...
	@docker-compose exec app uv run python manage.py migrate

# Create new Django database migrations
migrations:
	@echo Creating new migrations...
	@docker-compose exec app uv run python manage.py makemigrations

# Show pending migrations
showmigrations:
	@echo Showing migration status...
	@docker-compose exec app uv run python manage.py showmigrations

# Check for project issues
check:
	@echo Checking for project issues...
	@docker-compose exec app uv run python manage.py check

# Run the project test suite
test:
	@echo Running test suite...
	@docker-compose exec app uv run python manage.py test

# ------------------------------------
# Log Management
# ------------------------------------

# Display all services output logs
service-logs:
	@echo Streaming service logs \(Ctrl+C to exit\)...
	-@docker-compose logs -f

# View application logs (from logs/app.log)
app-logs:
	@echo Streaming application logs \(Ctrl+C to exit\)...
	@docker-compose exec app tail -f logs/app.log

# View error logs (from logs/errors.log)
error-logs:
	@echo Streaming error logs \(Ctrl+C to exit\)...
	@docker-compose exec app tail -f logs/errors.log

# View Django logs (from logs/django.log)
django-logs:
	@echo Streaming Django logs \(Ctrl+C to exit\)...
	@docker-compose exec app tail -f logs/django.log