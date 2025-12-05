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

- **Backend:** Django 5.2.8+ (Python 3.13)
- **Database:** SQLite3 (dev) / PostgreSQL (prod)
- **Cache:** Local Memory Cache (dev) / Redis (prod)
- **Admin Interface:** Django Unfold
- **Containerization:** Docker + Docker Compose

---

## 📁 Project Structure

```bash
crm-system/
├── .venv/                        # Python Virtual Environment (ignored by Git)
├── apps/                         # Django applications
│   ├── common/                   # Shared utilities across all apps
│   ├── security/                 # Authentication and security
│   └── users/                    # User management and authentication
├── config/                       # Django project settings
│   ├── formats/                  # Custom date/time formats by locale
│   ├── settings/                 # Split settings (base, dev, prod)
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── logs/                         # Application logs (ignored by Git)
│   ├── app.log                   # Application logs
│   ├── django.log                # Django framework logs
│   └── errors.log                # Error-only logs
├── media/                        # User-uploaded files
├── static/                       # Project-wide static files
├── staticfiles/                  # Collected static files for production
├── templates/                    # Project-wide HTML templates
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

   # Redis connection URL for production caching
   # Format: redis://HOST:PORT/DB_NUMBER
   # Example: redis://localhost:6379/0
   REDIS_URL=redis://localhost:6379/0

   # Directory where static files are collected for production
   # Absolute path (e.g., /var/www/static)
   STATIC_ROOT=/var/www/static

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

   After running `make setup-dev`, your containers are already running. To restart them later:
   ```bash
   make dev
    ```
  
  *(Access the application at `http://127.0.0.1:8000/` or `http://localhost:8000/`. The Django Admin panel is at `http://127.0.0.1:8000/admin/` (or your custom `ADMIN_URL` if set).)*

- **Production environment:**

   First, update your `.env` file:
   ```bash
   ENVIRONMENT=prod
   ```

   Then configure all required production variables: `SECRET_KEY`, `ALLOWED_HOSTS`, `ADMIN_URL`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `REDIS_URL`, `STATIC_ROOT`, `CSRF_TRUSTED_ORIGINS`.
  
   Finally, start production:
   ```bash
   make prod-build
   ```

  *(This builds production images with PostgreSQL, Redis, and Gunicorn.)*

---

## 💻 Custom Project Commands

### Initial Setup
```bash
make setup-dev                # Create initial setup for development
```

### Development
```bash
make dev                      # Start development environment
make dev-build                # Build and start development environment
make bash                     # Open container bash shell
make shell                    # Open Django shell
```

### Production
```bash
make prod                     # Start production environment
make prod-build               # Build and start production environment
```

### Database
```bash
make migrate                  # Apply database migrations
make migrations               # Create new migrations
make showmigrations           # Show migration status
```

### Application Management
```bash
make superuser                # Create Django superuser
make collectstatic            # Collect static files
make check                    # Check for project issues
make test                     # Run test suite
make manage.py cmd="..."      # Run custom manage.py command
```

### Container Management
```bash
make build                    # Build Docker images
make status                   # Show container status
make restart                  # Restart containers
make down                     # Stop and remove containers
make clean                    # Remove cache and OS-generated files
make reset                    # Remove ALL containers, volumes, and data
```

### Logs
```bash
make service-logs             # Show last 20 lines of service logs
make service-logs lines=50    # Show last 50 lines
make app-logs                 # View application logs
make error-logs               # View error logs
make django-logs              # View Django logs
```

---

## 📝 Notes

- **Development mode** uses SQLite by default and runs Django's development server with live code reload via volume mounting. Optional PostgreSQL and Redis support available.
- **Production mode** requires PostgreSQL and Redis, runs Gunicorn with immutable container images
- Logs are automatically rotated (max 10MB per file, 5 backups)
- Static files are served via WhiteNoise in production
- Session expires after 1 day or when browser closes
- **Note:** Make commands require at least one container to be running. If no containers are running, start with `make dev` or `make prod` first.