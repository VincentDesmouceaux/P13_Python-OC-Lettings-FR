"""
Fichier unique : DEV par défaut – PROD si DJANGO_DEBUG=false
Django 4.2 • Python 3.12
"""

from __future__ import annotations
import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict

# ───────────────────────── 1. BASE & .env ─────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv                # ≠ obligatoire en prod
    load_dotenv(BASE_DIR / ".env", override=False)
except ModuleNotFoundError:
    pass

# ───────────────────────── 2. CONTEXTE ────────────────────────────
RUNSERVER = "runserver" in sys.argv
RUNNING_TESTS = "pytest" in sys.argv[0] or "test" in sys.argv
DEBUG = (
    os.getenv("DJANGO_DEBUG", "").lower() == "true"             # variable explicite
    or (RUNSERVER and "DJANGO_DEBUG" not in os.environ)  # runserver sans var  → DEV
    or RUNNING_TESTS  # tests toujours DEV
)

# ───────────────────────── 3. CLÉS & HOSTS ───────────────────────
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "dev-secret"
        logging.warning("⚠️  SECRET_KEY de développement utilisée.")
    else:
        raise RuntimeError("DJANGO_SECRET_KEY manquant !")

# liste d’hôtes autorisés
raw_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(",") if h.strip()]

# Confort : runserver en « prod » → on ajoute localhost/0.0.0.0
if RUNSERVER and not DEBUG:
    for h in ("127.0.0.1", "0.0.0.0", "localhost"):
        if h not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(h)

if not DEBUG and not ALLOWED_HOSTS:
    raise RuntimeError("En production, DJANGO_ALLOWED_HOSTS ne peut pas être vide.")

# ───────────────────────── 4. APPS / MIDDLEWARE ──────────────────
INSTALLED_APPS = [
    "oc_lettings_site", "lettings", "profiles",
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
]

MIDDLEWARE = ["django.middleware.security.SecurityMiddleware"]

# WhiteNoise uniquement quand on est **réellement** en prod (pas runserver)
PROD = not DEBUG and not RUNSERVER and not RUNNING_TESTS
if PROD:
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "oc_lettings_site.urls"
WSGI_APPLICATION = "oc_lettings_site.wsgi.application"

# ───────────────────────── 5. TEMPLATES ──────────────────────────
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

# ───────────────────────── 6. BDD / I18N ─────────────────────────
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "oc-lettings-site.sqlite3"}
}
LANGUAGE_CODE, TIME_ZONE = "en-us", "UTC"
USE_I18N = USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ───────────────────────── 7. STATIC ─────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

if PROD:
    STORAGES = {
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    }
    WHITENOISE_KEEP_ONLY_HASHED_FILES = True
    WHITENOISE_MANIFEST_STRICT = True
else:
    STORAGES = {
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }

# ───────────────────────── 8. LOGGING ────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

# ───────────────────────── 9. SENTRY (optionnel) ────────────────
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[DjangoIntegration(),
                          LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)],
            traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE", "0.1")),
            environment="development" if DEBUG else "production",
            send_default_pii=False,
        )
    except ModuleNotFoundError:
        logging.warning("sentry-sdk absent : Sentry désactivé")

# ───────────────────────── 10. DIAGNOSTIC ────────────────────────
print(
    "\n".join([
        "=" * 80,
        f"Mode           : {'PROD' if PROD else 'DEV/TEST'}",
        f"DEBUG          : {DEBUG}",
        f"RUNSERVER      : {RUNSERVER}",
        f"Static backend : {STORAGES['staticfiles']['BACKEND']}",
        f"ALLOWED_HOSTS  : {ALLOWED_HOSTS}",
        "=" * 80,
    ])
)
