"""
Paramétrage unique
──────────────────
• DEV par défaut – passe en PROD quand DJANGO_DEBUG=false
• Statics :
    – DEV : servis depuis <projet>/static/
    – PROD : collectés dans <projet>/staticfiles/ (WhiteNoise compressé)
"""

from __future__ import annotations

import datetime
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict

# 0 ─────────────────────────────── .env ───────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv  # type: ignore
    # override=True → les valeurs du .env PRENNENT LE PAS sur l’environnement
    load_dotenv(BASE_DIR / ".env", override=True)
except ModuleNotFoundError:
    pass

# 1 ─────────────────────────── Contexte ───────────────────────────────
RUNSERVER = "runserver" in sys.argv
RUNNING_TESTS = "pytest" in sys.argv[0] or "test" in sys.argv


def _str2bool(val: str) -> bool:
    return val.lower() in {"1", "true", "yes", "y"}


if "DJANGO_DEBUG" in os.environ:                   # valeur explicite
    DEBUG: bool = _str2bool(os.environ["DJANGO_DEBUG"])
else:                                              # défaut : DEV
    DEBUG = True

PROD: bool = not DEBUG and not RUNNING_TESTS       # prod réel

# 2 ─────────────────────────── Clés & hosts ───────────────────────────
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
ALLOWED_HOSTS: list[str] = [
    h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()
]
if RUNSERVER and DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

# 3 ───────────────────── Apps & middleware ────────────────────────────
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

MIDDLEWARE = ["django.middleware.security.SecurityMiddleware"]
if PROD:                                           # WhiteNoise seulement en prod
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

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

# 4 ─────────────────────────── Templates ──────────────────────────────
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
            "oc_lettings_site.context_processors.sentry_dsn",
        ],
    },
}]

# 5 ─────────────────── Base de données & i18n ─────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "oc-lettings-site.sqlite3",
    }
}
LANGUAGE_CODE, TIME_ZONE = "en-us", "UTC"
USE_I18N = USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 6 ────────────────────── Fichiers statiques ──────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]     # sources
STATIC_ROOT = BASE_DIR / "staticfiles"       # artefacts collectés

if PROD:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        }
    }
else:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        }
    }

# 7 ─────────────────────────── Logging ────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

# 8 ─────────────────────────── Sentry ─────────────────────────────────
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    try:
        import sentry_sdk  # type: ignore
        from sentry_sdk.integrations.django import DjangoIntegration  # type: ignore
        from sentry_sdk.integrations.logging import LoggingIntegration  # type: ignore

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[
                DjangoIntegration(),
                LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
            ],
            traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE", "0.1")),
            environment="production" if PROD else "development",
            send_default_pii=False,
        )
    except ModuleNotFoundError:
        logging.warning("⚠️  sentry-sdk absent → Sentry désactivé")

# 9 ─────────────────── Bannière de démarrage ──────────────────────────
print(
    "\n".join(
        [
            "=" * 80,
            f"Mode        : {'PROD' if PROD else 'DEV'}",
            f"DEBUG       : {DEBUG}",
            f"Templates   : {BASE_DIR / 'templates'}",
            f"UTC start   : {datetime.datetime.utcnow().isoformat()}",
            "=" * 80,
        ]
    )
)
