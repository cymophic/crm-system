# CRM System

A modern Customer Relationship Management (CRM) system built with Django 5.2. Designed with scalability and maintainability in mind.

---

## 📚 Table of Contents
1. [⚙️ Technologies Used](#️-technologies-used)
2. [📁 Project Structure](#-project-structure)
3. [🚀 Getting Started](#-getting-started)
4. [💻 Custom Project Commands](#-custom-project-commands)

---

## ⚙️ Technologies Used

- **Frontend:** Tailwind CSS 4.x
- **Backend:** Django 5.2.8+ (Python 3.13)
- **Database:** SQLite3 (dev) / PostgreSQL (prod)
- **Cache & Message Broker:** Redis
- **Task Queue:** Celery
- **Admin Interface:** Django Unfold
- **Containerization:** Docker + Docker Compose

---

## 📁 Project Structure

```bash
crm-system/
├── .github/workflows/            # GitHub Actions workflows
├── .venv/                        # Python Virtual Environment (ignored by Git)
├── apps/                         # Django applications
│   ├── analytics/                # Analytics & dashboard
│   ├── base/                     # Core app
│   ├── common/                   # Shared utilities across all apps
│   │   └── templates/            # Reusable UI components
│   ├── security/                 # Authentication & account management
│   └── users/                    # User management
├── config/                       # Django project settings
│   ├── formats/                  # Custom date/time/number formats by locale
│   ├── settings/                 # Split settings (base, dev, prod)
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── celery.py                 # Celery instance setup
│   ├── constants.py              # Project-wide constants
│   ├── context_processors.py     # Custom template context processors
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── logs/
│   ├── app.log                   # Application logs
│   ├── django.log                # Django framework logs
│   └── errors.log                # Error-only logs
├── media/                        # User-uploaded files
├── static/                       # Project-wide static files
│   ├── css/
│   │   ├── tailwind/             # Tailwind CSS configuration
│   │   ├── base.css              # Base styles
│   │   ├── output.css            # Compiled Tailwind CSS
│   │   └── variables.css         # Defined CSS variables
│   └── js/
│       └── components/           # Component scripts (messages, navbar) 
├── staticfiles/                  # Collected static files for production
├── templates/                    # Project-wide HTML templates
│   ├── base.html                 # Master template
│   ├── components/               # Reusable UI components
│   └── layouts/                  # Layout templates
│       ├── app.html              # Main app layout
│       ├── auth.html             # Authentication pages layout
│       └── error.html            # Error pages layout
├── .dockerignore
├── .env                          # Environment variables (ignored by Git)
├── .env.example                  # Environment variables template
├── .gitignore
├── docker-compose.yml            # Docker services configuration
├── Dockerfile.dev                # Development Docker configuration
├── Dockerfile.prod               # Production Docker configuration
├── Makefile                      # Custom project commands
├── manage.py                     # Django management script
├── pyproject.toml                # Python dependencies
├── README.md
└── uv.lock                       # Dependency lockfile
```

---

## 🚀 Getting Started

### Prerequisites

- **Docker** and **Docker Compose** - [Get Docker](https://docs.docker.com/get-docker/)
- **Make** - Pre-installed on macOS/Linux, [Windows installation](https://gnuwin32.sourceforge.net/packages/make.htm)
- **Python 3.13** and **uv** - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

### Quick Start

```bash
git clone https://github.com/cymophic/crm-system.git
cd crm-system

cp .env.example .env
# Then configure your .env

make setup-dev
```

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cymophic/crm-system.git
   cd crm-system
   ```

2. **Configure your `.env` file:**

   Copy the `.env.example` file to `.env` in your project's root directory:
   
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` with your settings. See instructions for each environment variable:
   
   ```bash
   # --- Environment Mode ---
   # OPTIONS: 'dev' or 'development' | 'prod' or 'production'
   # This controls which Docker Compose profile and Dockerfile are used
   ENVIRONMENT=dev

   # --- Django Core Settings ---
   # Generate a new key with CLI command: 
   # python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   # DEV: Leave empty to auto-generate | PROD: Required
   SECRET_KEY=

   # Allowed Hosts: Comma-separated list of hostnames/domains Django can serve.
   # DEV: Auto-adds localhost/127.0.0.1 | PROD: Required
   # For production: yourwebsite.com,www.yourwebsite.com
   ALLOWED_HOSTS=

   # --- Admin Configuration ---
   # Custom admin URL path (security through obscurity)
   # DEV: Defaults to 'admin/' if empty | PROD: Required
   ADMIN_URL=

   # --- SSL Configuration ---
   # Set to True only when running with valid SSL certificate
   ENABLE_SSL=False

   # --- Redis Configuration ---
   # Redis connection URL for caching (used in both dev and prod)
   # Format: redis://HOST:PORT/DB_NUMBER
   # For Docker: redis://redis:6379/0
   # For local: redis://localhost:6379/0
   REDIS_URL=redis://redis:6379/0

   # --- Email Configuration ---
   # Hostname of the email provider's SMTP server
   EMAIL_HOST=smtp.gmail.com

   # Port number for SMTP connection (587 for TLS, 465 for SSL)
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_USE_SSL=False

   # The full email address used to send emails
   EMAIL_HOST_USER=your_email@gmail.com

   # Secure app password (not your main account password)
   # For Gmail: https://support.google.com/accounts/answer/185833
   EMAIL_HOST_PASSWORD=your_app_password_here

   # --- Email Recipients ---
   # Comma-separated list of helpdesk email addresses
   EMAIL_HELPDESK=helpdesk@yourdomain.com,help@example.com

   # Comma-separated list of admin email addresses
   EMAIL_ADMIN=admin@yourdomain.com,admin@example.com

   # --- Development Database ---
   # Local Development Database: Uses SQLite3 (no setup required)
   # Leave empty to use default: sqlite:///db.sqlite3
   DATABASE_DEV=sqlite:///db.sqlite3

   # --- Production Settings (required in prod) ---
   # PostgreSQL Credentials: Get these from your hosting provider
   POSTGRES_DB=your_database_name
   POSTGRES_USER=your_database_user
   POSTGRES_PASSWORD=your_database_password

   # Directory where static files are collected for production
   # Absolute path (e.g., /app/staticfiles)
   STATIC_ROOT=/app/staticfiles

   # Comma-separated list of admin email addresses for error notifications
   # Format: name@domain.com,another@domain.com
   ADMINS=admin@yourdomain.com

   # Comma-separated list of trusted origins for CSRF protection
   # Format: https://example.com,https://www.example.com
   CSRF_TRUSTED_ORIGINS=https://yourwebsite.com,https://www.yourwebsite.com
   ```

3. **Run initial setup:**

   This command creates containers, applies database migrations, and creates a superuser:
   
   ```bash
   make setup-dev
   ```
   
   Follow the prompts to set up your admin credentials (username, email, password).

### Running the Application

- **Development environment:**

   After running `make setup-dev`, your containers are already running. To start them next time:
   ```bash
   make dev
    ```

- **Production environment:**

   First, update your `.env` file:
   ```bash
   ENVIRONMENT=prod
   ```

   Then configure all required production variables: `SECRET_KEY`, `ALLOWED_HOSTS`, `ADMIN_URL`, `ENABLE_SSL`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `REDIS_URL`, `STATIC_ROOT`, `CSRF_TRUSTED_ORIGINS`.
  
   Finally, start production:
   ```bash
   make setup-prod
   ```

---

## 💻 Custom Project Commands

### Initial Setup
```bash
make setup-dev                    # Create initial setup for development
make setup-prod                   # Create initial setup for production
```

### Development
```bash
make dev                          # Start development environment
make dev-build                    # Build and start development environment
make bash                         # Open container bash shell
make shell                        # Open Django shell
```

### Production
```bash
make prod                         # Start production environment
make prod-build                   # Build and start production environment
make security-status              # Run security configuration checks
```

### Database
```bash
make migrate                      # Apply database migrations
make migrations                   # Create new migrations
make showmigrations               # Show migration status
```

### Container Management
```bash
make build                        # Build Docker images
make status                       # Show container status
make restart                      # Restart containers
make down                         # Stop and remove containers
make clean                        # Remove cache and OS-generated files
make reset                        # Remove ALL containers, volumes, and data
```

### Application Management
```bash
make superuser                    # Create Django superuser
make collectstatic                # Collect static files
make check                        # Check for project issues
make test                         # Run test suite
make build-css                    # Build minified CSS for production
make manage.py cmd="..."          # Run custom manage.py command
```

### Task Management
```bash
make celery-worker                # Start Celery worker
make celery-status                # Check Celery worker status
```

### Logs
```bash
# View main container logs
make service-logs                 # View environment container logs
make service-logs follow=true     # Follow logs in real-time

# View specific service logs
make service-logs service=db      # View PostgreSQL database logs
make service-logs service=celery  # View Celery logs
make service-logs service=redis   # View Redis logs

# View application file logs
make app-logs                     # View logs/app.log
make error-logs                   # View logs/errors.log
make django-logs                  # View logs/django.log

# View more/fewer lines (default: 20)
make app-logs lines=10
make service-logs service=db lines=100

# Combine options
make service-logs lines=50 follow=true
make service-logs service=celery follow=true
```

---

## 📝 Notes

- **Development mode** uses SQLite, Redis, and Celery by default, runs Django's development server with live code reload via volume mounting. Optional PostgreSQL support available.
- **Production mode** requires PostgreSQL, Redis, and Celery, runs Gunicorn with immutable container images
- **Application file logs** are automatically rotated (max 10MB per file, 5 backups)
- **Make commands** require at least one container to be running. If no containers are running, start with `make dev` or `make prod` first.