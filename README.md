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

- **Backend:** Django 5.2.8 (Python 3.13)
- **Database:** SQLite3 (dev) / PostgreSQL (prod)
- **Cache:** Local Memory Cache (dev) / Redis (prod)
- **Admin Interface:** Django Unfold
- **Containerization:** Docker + Docker Compose

---

## 📁 Project Structure

```
crm-system/
├── .venv/                        # Python Virtual Environment (ignored by Git)
├── apps/                         # Django applications
│   ├── common/                   # Shared utilities across all apps
│   └── users/                    # User management and authentication
├── config/                       # Django project settings
│   └── settings/                 # Split settings (base, dev, prod)
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       └── prod.py
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
├── docker-entrypoint.sh          # Container startup script
├── Dockerfile
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

### Quick Start

```bash
git clone https://github.com/cymophic/crm-system.git
cd crm-system

cp .env.example .env
# Then configure your .env

make setup-dev
```

### Configuration

Edit `.env` with your settings. Key variables:

```bash
# Environment: 'dev' or 'prod'
ENVIRONMENT=dev

# Security (auto-generated in dev if empty)
SECRET_KEY=
ALLOWED_HOSTS=

# Admin panel URL (defaults to 'admin/' in dev)
ADMIN_URL=

# Email Configuration (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Development Database (defaults to SQLite)
DATABASE_DEV=sqlite:///db.sqlite3

# Production Settings (required in prod)
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
REDIS_URL=redis://localhost:6379/0
STATIC_ROOT=/var/www/static
```

See `.env.example` for complete configuration details.

---

## 💻 Custom Project Commands

### Initial Setup
```bash
make setup-dev           # Complete setup for development (builds, migrates, creates superuser)
```

### Development
```bash
make dev                 # Start development environment
make dev-build           # Build and start development environment
make bash                # Open container bash shell
make shell               # Open Django shell
```

### Production
```bash
make prod                # Start production environment
make prod-build          # Build and start production environment
```

### Database
```bash
make migrate             # Apply database migrations
make migrations          # Create new migrations
make showmigrations      # Show migration status
```

### Application Management
```bash
make superuser           # Create Django superuser
make collectstatic       # Collect static files
make check               # Check for project issues
make test                # Run test suite
```

### Container Management
```bash
make build               # Build Docker images
make status              # Show container status
make restart             # Restart containers
make down                # Stop and remove containers
make clean               # Remove cache files (.pyc, __pycache__, etc.)
make reset               # Remove ALL containers, volumes, and data (⚠️ WARNING)
```

### Logs
```bash
make service-logs        # Stream all service logs
make app-logs            # View application logs
make error-logs          # View error logs
make django-logs         # View Django logs
```

---

## 📝 Notes

- **Development mode** uses SQLite and runs Django's development server
- **Production mode** uses PostgreSQL, Redis, and Gunicorn
- Logs are automatically rotated (max 10MB per file, 5 backups)
- Static files are served via WhiteNoise in production
- Session expires after 1 day or when browser closes