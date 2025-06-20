"""
Django 4.2 – configuration **uniquement DEV / TEST**.

• DEBUG est toujours à True (sauf si DJANGO_DEBUG=false explicitement).
• AUCUN ManifestStaticFilesStorage → plus d’erreurs « Missing manifest ».
• Pas de WhiteNoise ; runserver sert /static/ directement.
"""

from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Any, Dict


# ─────────── BASE / .env ───────────
BASE_DIR = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv   # type: ignore
    load_dotenv(BASE_DIR / ".env", override=False)
except ModuleNotFoundError:
    pass

# ─────────── DEBUG toujours True sauf si override ───────────
# Correction : FORCER DEBUG=True en mode développement
DEBUG = True if 'runserver' in sys.argv else os.getenv("DJANGO_DEBUG", "true").lower() == "true"
RUNNING_TESTS = "pytest" in sys.argv[0] or "test" in sys.argv

# ─────────── CLÉS & HOSTS ───────────
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost"
).split(",")

# ─────────── APPS & MIDDLEWARE (sans WhiteNoise) ───────────
INSTALLED_APPS = [
    "oc_lettings_site",
    "lettings",
    "profiles",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "oc_lettings_site.urls"
WSGI_APPLICATION = "oc_lettings_site.wsgi.application"

# ─────────── TEMPLATES ───────────
TEMPLATES: list[Dict[str, Any]] = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
    },
}]

# ─────────── DB / I18N ───────────
DATABASES = {"default": {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "oc-lettings-site.sqlite3",
}}
LANGUAGE_CODE, TIME_ZONE = "en-us", "UTC"
USE_I18N = USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─────────── STATIC : configuration corrigée ───────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
# Correction : STATIC_ROOT doit être différent de STATICFILES_DIRS
STATIC_ROOT = BASE_DIR / "static_collected"

# Correction : Configuration de stockage simplifiée
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# ─────────── LOGGING simple ───────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

# Correction : Forcer DEBUG=True si le serveur est lancé avec runserver
if 'runserver' in sys.argv and not DEBUG:
    DEBUG = True
    print("!!! DEBUG forcé à True pour le serveur de développement !!!")

print(
    f"=== MODE DEV – DEBUG={DEBUG} – STATICFILES_STORAGE={STORAGES['staticfiles']['BACKEND']} ===")
