"""
Réglage « tout-en-un » :
• DEV par défaut – PROD si DJANGO_DEBUG=false
• WhiteNoise actif et *relaxed* en PROD
"""

from __future__ import annotations
import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict

# ─────────────── 0. .env ───────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv(BASE_DIR / ".env", override=False)
except ModuleNotFoundError:
    pass

# ─────────────── 1. contexte ──────────────────────────────────────────
RUNSERVER = "runserver" in sys.argv
RUNNING_TESTS = "pytest" in sys.argv[0] or "test" in sys.argv
DEBUG = os.getenv("DJANGO_DEBUG", "").lower() == "true" or (
    RUNSERVER and "DJANGO_DEBUG" not in os.environ) or RUNNING_TESTS
PROD = not DEBUG and not RUNSERVER and not RUNNING_TESTS

# ─────────────── 2. secrets / hosts ───────────────────────────────────
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost,0.0.0.0"
    ).split(",") if h.strip()
]
if RUNSERVER and not DEBUG:        # confort pour « runserver --insecure »
    ALLOWED_HOSTS += ["127.0.0.1", "0.0.0.0", "localhost"]

# ─────────────── 3. apps / middleware ────────────────────────────────
INSTALLED_APPS = [
    "oc_lettings_site", "lettings", "profiles",
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware"]
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

# ─────────────── 4. templates ────────────────────────────────────────
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

# ─────────────── 5. BDD & i18n ───────────────────────────────────────
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3",
                         "NAME": BASE_DIR / "oc-lettings-site.sqlite3"}}
LANGUAGE_CODE, TIME_ZONE = "en-us", "UTC"
USE_I18N = USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─────────────── 6. static ───────────────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
if PROD:
    STORAGES = {"staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"}}
else:
    STORAGES = {"staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}

# ─────────────── 7. logs ─────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING: Dict[str, Any] = {
    "version": 1, "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

# ─────────────── 8. Sentry (facultatif) ──────────────────────────────
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    try:
        import sentry_sdk  # type: ignore
        from sentry_sdk.integrations.django import DjangoIntegration  # type: ignore
        from sentry_sdk.integrations.logging import LoggingIntegration  # type: ignore
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[DjangoIntegration(),
                          LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)],
            traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE", "0.1")),
            environment="development" if DEBUG else "production",
            send_default_pii=False,
        )
    except ModuleNotFoundError:
        logging.warning("sentry-sdk non installé → Sentry désactivé")

# ─────────────── 9. diagnostic console ──────────────────────────────
print("\n".join(["="*80,
      f"Mode           : {'PROD' if PROD else 'DEV/TEST'}",
      f"DEBUG          : {DEBUG}",
      f"RUNSERVER      : {RUNSERVER}",
      f"Static backend : {STORAGES['staticfiles']['BACKEND']}",
      f"ALLOWED_HOSTS  : {ALLOWED_HOSTS}", "="*80]))
