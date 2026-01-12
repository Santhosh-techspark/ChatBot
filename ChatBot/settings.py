import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# ==================================================
# Base directory
# ==================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# Load environment variables ONCE
# ==================================================
load_dotenv(BASE_DIR / ".env")

# ==================================================
# Django core settings
# ==================================================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY",
                       "django-insecure-change-this-in-production")

DEBUG = True
ALLOWED_HOSTS = ["*"]

# ==================================================
# Installed applications
# ==================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "chatbotapp.apps.ChatbotappConfig",
]

# ==================================================
# Middleware
# ==================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==================================================
# URLs & Templates
# ==================================================
ROOT_URLCONF = "ChatBot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "ChatBot.wsgi.application"

# ==================================================
# Database (PostgreSQL) - Replit configuration
# ==================================================

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL,
                                          conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("PGDATABASE",
                              os.getenv("POSTGRES_DB", "chatbotdb")),
            "USER": os.getenv("PGUSER", os.getenv("POSTGRES_USER",
                                                  "postgres")),
            "PASSWORD": os.getenv("PGPASSWORD",
                                  os.getenv("POSTGRES_PASSWORD", "")),
            "HOST": os.getenv("PGHOST", os.getenv("POSTGRES_HOST",
                                                  "localhost")),
            "PORT": os.getenv("PGPORT", os.getenv("POSTGRES_PORT", "5432")),
        }
    }

# ==================================================
# CSRF Configuration for Replit proxy
# ==================================================
CSRF_TRUSTED_ORIGINS = [
    "https://*.replit.app",
]

# ==================================================
# Password validation
# ==================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

# ==================================================
# Internationalization
# ==================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ==================================================
# Static files (CSS, JavaScript, Images)
# ==================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==================================================
# Authentication redirects
# ==================================================
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# ==================================================
# Default primary key field
# ==================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==================================================
# 🔑 AI API Keys (DO NOT hardcode)
# ==================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
