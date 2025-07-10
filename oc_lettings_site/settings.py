"""
Django settings – sécurisées pour déploiement Northflank / Code.run
-------------------------------------------------------------------
• Les valeurs sensibles (SECRET_KEY, hôtes, DSN…) sont **uniquement** lues depuis
  les variables d’environnement.
• Les domaines autorisés et les origines CSRF sont entières‑ment configurables
  sans modifier ce fichier.
"""

from __future__ import annotations

import datetime
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# ─────────────────────────── 0. .env (facultatif) ─────────────────────
BASE_DIR: Path = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv  # type: ignore
    # override=True : les variables du .env *écrasent* l’environnement
    load_dotenv(BASE_DIR / ".env", override=True)
except ModuleNotFoundError:
    pass

# ─────────────────────────── 1. Contexte d’exécution ──────────────────
RUNSERVER = "runserver" in sys.argv
RUNNING_TESTS = "pytest" in sys.argv[0] or "test" in sys.argv


def str2bool(val: str | None, *, default: bool = False) -> bool:
    if val is None:
        return default
    return val.lower() in {"1", "true", "yes", "y"}


def csv_env(var: str) -> List[str]:
    """Renvoie une liste nettoyée depuis une variable d’env séparée par des virgules."""
    return [v.strip() for v in os.getenv(var, "").split(",") if v.strip()]


DEBUG: bool = str2bool(os.getenv("DJANGO_DEBUG"), default=True)
PROD: bool = not DEBUG and not RUNNING_TESTS

# ─────────────────────────── 2. Clés & hosts ──────────────────────────
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY must be set!")

ALLOWED_HOSTS: List[str] = csv_env("DJANGO_ALLOWED_HOSTS")

# Autorise toujours les prévisualisations locales `manage.py runserver`
if RUNSERVER and DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

if PROD and not ALLOWED_HOSTS:
    raise RuntimeError("DJANGO_ALLOWED_HOSTS must be set in production!")

# CSRF : domains sûrs (schéma requis)
CSRF_TRUSTED_ORIGINS: List[str] = csv_env("DJANGO_CSRF_TRUSTED_ORIGINS")
if not CSRF_TRUSTED_ORIGINS and ALLOWED_HOSTS:
    # Derive automatiquement : https://<host>  (ignore localhost & cie)
    CSRF_TRUSTED_ORIGINS = [
        f"https://{h.lstrip('*.')}" for h in ALLOWED_HOSTS
        if h not in {"127.0.0.1", "localhost", "0.0.0.0"}
    ]

if PROD and not CSRF_TRUSTED_ORIGINS:
    raise RuntimeError("DJANGO_CSRF_TRUSTED_ORIGINS must be set in production!")

# Derrière un proxy SSL (Northflank, Railway, Render…)
if str2bool(os.getenv("DJANGO_BEHIND_PROXY"), default=True):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = PROD
SESSION_COOKIE_SECURE = PROD
CSRF_COOKIE_SECURE = PROD

# ───────────────────── 3. Apps & middleware ───────────────────────────
INSTALLED_APPS = [
    "oc_lettings_site",
    "lettings",
    "profiles",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE: List[str] = ["django.middleware.security.SecurityMiddleware"]

# WhiteNoise seulement en PROD pour le manifest compressé
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

# ─────────────────────────── 4. Templates ─────────────────────────────
TEMPLATES: List[Dict[str, Any]] = [
    {
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
    }
]

# ───────────────────── 5. BDD & i18n ──────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DJANGO_DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DJANGO_DB_NAME", BASE_DIR / "oc-lettings-site.sqlite3"),
        "USER": os.getenv("DJANGO_DB_USER", ""),
        "PASSWORD": os.getenv("DJANGO_DB_PASSWORD", ""),
        "HOST": os.getenv("DJANGO_DB_HOST", ""),
        "PORT": os.getenv("DJANGO_DB_PORT", ""),
    }
}

LANGUAGE_CODE = os.getenv("DJANGO_LANGUAGE_CODE", "en-us")
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_I18N = USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ────────────────────── 6. Fichiers statiques ─────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # sources en DEV
STATIC_ROOT = BASE_DIR / "staticfiles"     # collectstatic en PROD

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

# ─────────────────────────── 7. Logging ───────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

# ─────────────────────────── 8. Sentry (optionnel) ───────────────────
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
        logging.warning("⚠️  sentry-sdk non installé → Sentry désactivé")

# ─────────────────── 9. Bannière de démarrage ─────────────────────────
print("\n".join([
    "=" * 80,
    f"Mode        : {'PROD' if PROD else 'DEV'}",
    f"DEBUG       : {DEBUG}",
    f"ALLOWED     : {', '.join(ALLOWED_HOSTS) or '<aucun>'}",
    f"CSRF Origin : {', '.join(CSRF_TRUSTED_ORIGINS) or '<aucun>'}",
    f"UTC start   : {datetime.datetime.utcnow().isoformat()}",
    "=" * 80,
]))
