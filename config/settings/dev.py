import dj_database_url
from decouple import Csv, config
from django.core.management.utils import get_random_secret_key

from .base import *

# ------------------------------------
# Debug Mode
# ------------------------------------
DEBUG = True

# ------------------------------------
# Security
# ------------------------------------
SECRET_KEY = config("SECRET_KEY", default="") or get_random_secret_key()

# Allowed Hosts
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
ALLOWED_HOSTS += ["127.0.0.1", "localhost"]
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

# Cookie Security
SESSION_COOKIE_SECURE = ENABLE_SSL
CSRF_COOKIE_SECURE = ENABLE_SSL
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Content Security Policy
CSP_REPORT_ONLY = True
CONTENT_SECURITY_POLICY = CONTENT_SECURITY_POLICY.copy()
CONTENT_SECURITY_POLICY["DIRECTIVES"] = CONTENT_SECURITY_POLICY["DIRECTIVES"].copy()

# ------------------------------------
# Database
# ------------------------------------
DATABASE_DEV = (
    config("DATABASE_DEV", default="sqlite:///db.sqlite3") or "sqlite:///db.sqlite3"
)
DATABASES = {"default": dj_database_url.parse(DATABASE_DEV)}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 50000

# ------------------------------------
# Sessions
# ------------------------------------
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# ------------------------------------
# Logging
# ------------------------------------
LOGGING["handlers"]["console"]["level"] = "DEBUG"
LOGGING["loggers"]["apps"]["level"] = "DEBUG"
