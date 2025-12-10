import dj_database_url
from decouple import Csv, config

from .base import *

# ------------------------------------
# Debug Mode
# ------------------------------------
DEBUG = False

# ------------------------------------
# Security
# ------------------------------------
SECRET_KEY = config("SECRET_KEY")

# Allowed Hosts
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# SSL Redirect
SECURE_SSL_REDIRECT = ENABLE_SSL

# Cookie Security
SESSION_COOKIE_SECURE = ENABLE_SSL
CSRF_COOKIE_SECURE = ENABLE_SSL
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000 if ENABLE_SSL else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = ENABLE_SSL
SECURE_HSTS_PRELOAD = ENABLE_SSL

# Content Security
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Referrer Policy
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

# CSRF & Trusted Origins
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())

# Content Security Policy
CSP_REPORT_ONLY = False
CONTENT_SECURITY_POLICY = CONTENT_SECURITY_POLICY.copy()
CONTENT_SECURITY_POLICY["DIRECTIVES"] = CONTENT_SECURITY_POLICY["DIRECTIVES"].copy()

# ------------------------------------
# Admin
# ------------------------------------
ADMINS = config("ADMINS", default="", cast=Csv())

# ------------------------------------
# Database
# ------------------------------------

# Credentials
POSTGRES_DB = config("POSTGRES_DB")
POSTGRES_USER = config("POSTGRES_USER")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")

# Build Connection URL
DATABASE_PROD = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
)

# Parse and configure database
DATABASES = {"default": dj_database_url.parse(DATABASE_PROD, conn_max_age=600)}

# ------------------------------------
# Sessions
# ------------------------------------
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"

# ------------------------------------
# Logging
# ------------------------------------
LOGGING["handlers"]["console"]["level"] = "WARNING"
LOGGING["loggers"]["apps"]["level"] = "INFO"
