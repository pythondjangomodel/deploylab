"""
Django settings for deploylab project.

This file is intentionally written to work in TWO modes:
1. Local development on your Windows machine (DEBUG=True, SQLite)
2. Production on Render (DEBUG=False, Postgres, env vars)

Everything that changes between the two is read from environment
variables, so the same settings.py file works in both places.
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------
# SECURITY
# --------------------------------------------------------------------
# Locally, if SECRET_KEY isn't set, fall back to a dev-only key.
# On Render, you MUST set SECRET_KEY as an environment variable.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "dev-only-insecure-key-change-me-CHANGE-ME-123456"
)

# Locally this defaults to True. On Render, set DEBUG=False as an env var.
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Locally this stays empty (not needed when DEBUG=True).
# On Render, set ALLOWED_HOSTS=your-app-name.onrender.com
ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()
]
if DEBUG:
    ALLOWED_HOSTS += ["localhost", "127.0.0.1"]

# Render sets this automatically for each deploy; used to auto-allow
# the *.onrender.com host without you having to hardcode it.
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h not in ("localhost", "127.0.0.1")]

# --------------------------------------------------------------------
# APPLICATIONS
# --------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "notes",
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise serves static files directly from Django in production,
    # so we don't need a separate Nginx server for this small project.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "deploylab.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "deploylab.wsgi.application"

# --------------------------------------------------------------------
# DATABASE
# --------------------------------------------------------------------
# Locally: falls back to SQLite (zero setup needed on Windows).
# On Render: reads DATABASE_URL env var and connects to Postgres.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------
# STATIC FILES (CSS, JS) — served by WhiteNoise in production
# --------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"   # collectstatic gathers files here
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --------------------------------------------------------------------
# MEDIA FILES (user-uploaded images)
# --------------------------------------------------------------------
# NOTE: Render's free tier has an EPHEMERAL filesystem — uploaded files
# are wiped on every redeploy/restart. This works fine for local testing
# and for learning, but for a real production app you'd swap this for
# cloud storage (e.g. Cloudinary or S3). That's a deliberate "gotcha"
# left in this project for you to discover and research yourself.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
