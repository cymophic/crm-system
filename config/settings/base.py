from pathlib import Path

from csp.constants import NONE, SELF
from decouple import Csv, config
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# ------------------------------------
# Base Directory
# ------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ------------------------------------
# Security
# ------------------------------------
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": [SELF],
        "script-src": [
            SELF,
            "'unsafe-inline'",
            "'unsafe-eval'",
        ],
        "style-src": [SELF, "'unsafe-inline'"],
        "img-src": [SELF, "data:"],
        "font-src": [SELF],
        "connect-src": [SELF],
        "frame-ancestors": [NONE],
    },
}

# ------------------------------------
# Database
# ------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------
# Application
# ------------------------------------
INSTALLED_APPS = [
    # Initial Apps
    "django.contrib.sites",
    # Project Apps
    "apps.common",
    "apps.security",
    "apps.users",
    # Third-party Packages
    "unfold",
    "django_tailwind_cli",
    "phonenumber_field",
    "djmoney",
    # Core Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

# ------------------------------------
# Middleware
# ------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "csp.middleware.CSPMiddleware",  # django-csp
    "whitenoise.middleware.WhiteNoiseMiddleware",  # whitenoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # core-django-i18n
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_currentuser.middleware.ThreadLocalUserMiddleware",  # django-currentuser
]

# ------------------------------------
# URL & WSGI
# ------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------
# Authentication
# ------------------------------------
AUTH_USER_MODEL = "users.User"
SITE_ID = 1  # django.contrib.sites

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ------------------------------------
# Sessions
# ------------------------------------
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 86400  # 1 day in seconds
SESSION_SAVE_EVERY_REQUEST = True

# ------------------------------------
# Templates
# ------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ------------------------------------
# Static & Media Files
# ------------------------------------
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = (
    config("STATIC_ROOT", default=BASE_DIR / "staticfiles") or BASE_DIR / "staticfiles"
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------
# Internationalization
# ------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True
FORMAT_MODULE_PATH = [
    "config.formats",
]

# Phone Numbers
PHONENUMBER_DEFAULT_REGION = "PH"  # django-phonenumber-field

# Currency
CURRENCIES = ("PHP", "USD")  # django-money
DEFAULT_CURRENCY = "PHP"  # django-money
CURRENCY_CHOICES = [  # django-money
    ("PHP", "₱"),
    ("USD", "$"),
]

# ------------------------------------
# Email Configuration
# ------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = f"CRM System <{EMAIL_HOST_USER}>"

# Email Recipients
EMAIL_HELPDESK = config("EMAIL_HELPDESK", default="", cast=Csv())
EMAIL_ADMIN = config("EMAIL_ADMIN", default="", cast=Csv())

# ------------------------------------
# Logging
# ------------------------------------
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)  # Create logs folder if non-existent

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # Define how log messages are formatted
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",  # 2025-11-02 14:30:45
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    # Define where logs are sent
    "handlers": {
        # Console output
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        # Django framework logs
        "django_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "django.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        # Application logs
        "app_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "app.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        # Error-only log file
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "errors.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    # Configure loggers for different parts of the application
    "loggers": {
        "django": {
            "handlers": ["console", "django_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["error_file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "apps": {
            "handlers": ["app_file", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    # Default handler for any messages not captured by loggers
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# ------------------------------------
# Unfold Admin Configuration
# ------------------------------------
UNFOLD = {
    "SITE_TITLE": "CRM Admin",
    "SITE_HEADER": "CRM Admin",
    "SITE_SUBHEADER": "Customer Relationship Management System",
    "THEME": "light",
    "SITE_URL": "/",
    "COLORS": {
        "primary": {
            "50": "#fafafa",
            "100": "#f5f5f5",
            "200": "#e5e5e5",
            "300": "#d4d4d4",
            "400": "#a3a3a3",
            "500": "#737373",
            "600": "#525252",
            "700": "#404040",
            "800": "#262626",
            "900": "#171717",
            "950": "#0a0a0a",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Overview"),
                "items": [
                    {
                        "link": reverse_lazy("admin:index"),
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "permission": lambda request: request.user.is_authenticated,
                    },
                ],
            },
            {
                "title": _("Users & Roles"),
                "collapsible": True,
                "permission": lambda request: request.user.is_superuser,
                "items": [
                    {
                        "link": reverse_lazy("admin:users_user_changelist"),
                        "title": _("Users"),
                        "icon": "person",
                        "permission": lambda request: request.user.is_authenticated,
                    },
                    {
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "title": _("Groups"),
                        "icon": "admin_panel_settings",
                        "permission": lambda request: request.user.is_authenticated,
                    },
                ],
            },
            {
                "title": _("System Settings"),
                "collapsible": True,
                "permission": lambda request: request.user.is_superuser,
                "items": [
                    {
                        "link": reverse_lazy("admin:sites_site_changelist"),
                        "title": _("Sites"),
                        "icon": "web",
                        "permission": lambda request: request.user.is_authenticated,
                    },
                ],
            },
        ],
    },
}

# ------------------------------------
# Django Tailwind CLI Configuration
# ------------------------------------
TAILWIND_CLI_ARGS = "--minify"
