"""
Django settings for oc_lettings_site (compatible Django 4.2 LTS / Python 3.12).
Seules les options utiles au projet de démonstration sont conservées.
"""

from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import os

SENTRY_DSN = os.getenv("SENTRY_DSN", None)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        # Capture 100% des erreurs en prod (ajustez en fonction de votre plan)
        traces_sample_rate=1.0,
        send_default_pii=False,  # ne pas envoyer d’info personnelle
    )

# oc_lettings_site/settings.py

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        # Sentry captera automatiquement les erreurs via DjangoIntegration
    },
    "loggers": {
        "": {  # logger racine
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",  # on logge les 500
            "propagate": False,
        },
        "lettings": {
            "handlers": ["console"],
            "level": "DEBUG",  # ou INFO en prod
            "propagate": True,
        },
        "profiles": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


# ----- BASE -----
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "fp$9^593hsriajg$_%=5trot9g!1qa@ew(o-1#@=&4%=hp46(s"
DEBUG = False
ALLOWED_HOSTS = ["*"]   # le temps des tests


# ----- APPLICATIONS -----
INSTALLED_APPS = [
    # Apps projet (on ajoutera lettings & profiles plus tard)
    "oc_lettings_site.apps.OCLettingsSiteConfig",
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "lettings.apps.LettingsConfig",
    "profiles.apps.ProfilesConfig",

]

# ----- MIDDLEWARE -----
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

]

ROOT_URLCONF = "oc_lettings_site.urls"
WSGI_APPLICATION = "oc_lettings_site.wsgi.application"

# ----- TEMPLATES -----
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],          # dossier global
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

# ----- BASE DE DONNÉES -----
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "oc-lettings-site.sqlite3",
    }
}

# ----- AUTH / SÉCURITÉ -----
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ----- INTERNATIONALISATION -----
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True           # USE_L10N a été supprimé depuis Django 4.0

# ----- FICHIERS STATIQUES -----

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

WHITENOISE_MANIFEST_STRICT = False  # Add this line


# ----- DJANGO 4.2+ : champ auto par défaut -----
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
