"""
oc_lettings_site/settings.py
────────────────────────────
Django 4.2 / Python 3.12

• Toutes les valeurs dépendantes de l’environnement sont lues via `os.getenv`
  (12-factor).
• Sentry est initialisé si – et seulement si – `SENTRY_DSN` est présent.  
• Un **seul** bloc LOGGING : – aucune re-définition – afin d’éviter les
  erreurs `Unable to configure formatter 'standard'`.
"""

from pathlib import Path
import os
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# ─────────────────────────────────────────────────────────── 1. BASE
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "⚠️-change-me-in-prod-⚠️")
DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",        # « nom1,nom2 » en prod
    "127.0.0.1,localhost"          # par défaut en local
).split(",")

# ─────────────────────────────────────────────────────────── 2. APPS
INSTALLED_APPS = [
    "oc_lettings_site.apps.OCLettingsSiteConfig",
    "lettings.apps.LettingsConfig",
    "profiles.apps.ProfilesConfig",

    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# ─────────────────────────────────────────────────────────── 3. MIDDLEWARE
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

# ─────────────────────────────────────────────────────────── 4. TEMPLATES
TEMPLATES = [
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
                # Expose éventuellement la DSN aux templates
                "oc_lettings_site.context_processors.sentry_dsn",
            ],
        },
    },
]

# ─────────────────────────────────────────────────────────── 5. DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "oc-lettings-site.sqlite3",
    }
}

# ─────────────────────────────────────────────────────────── 6. AUTH / I18N
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─────────────────────────────────────────────────────────── 7. STATIC
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ─────────────────────────────────────────────────────────── 8. LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name}: {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # Ce handler n’est ajouté que si Sentry est activé (voir plus bas)
        "sentry": {
            "class": "sentry_sdk.integrations.logging.EventHandler",
            "level": "ERROR",
        },
    },

    "root": {  # logger racine
        "handlers": ["console", "sentry"],
        "level": os.getenv("LOG_LEVEL", "INFO"),
    },

    "django.request": {
        "handlers": ["console", "sentry"],
        "level": "ERROR",
        "propagate": False,
    },

    # log applicatifs
    "profiles": {"handlers": ["console"], "level": "INFO", "propagate": True},
    "lettings":  {"handlers": ["console"], "level": "INFO", "propagate": True},
}

# ─────────────────────────────────────────────────────────── 9. SENTRY
SENTRY_DSN: str | None = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
        ],
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE", "0.1")),
        send_default_pii=True,
    )
    logging.getLogger(__name__).info(
        "Sentry initialisé – mode %s", "DEBUG" if DEBUG else "PROD"
    )
else:
    # si le DSN n’existe pas, on retire le handler « sentry » pour éviter l’erreur
    LOGGING["handlers"].pop("sentry")
    LOGGING["root"]["handlers"].remove("sentry")
    LOGGING["django.request"]["handlers"].remove("sentry")
    logging.getLogger(__name__).warning("Sentry désactivé (SENTRY_DSN manquant)")
