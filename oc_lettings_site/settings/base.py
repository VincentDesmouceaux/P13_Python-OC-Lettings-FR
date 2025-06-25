from __future__ import annotations
import os
import logging
import datetime
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ─────────────── .env facultatif ───────────────
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv(BASE_DIR / ".env", override=False)
except ModuleNotFoundError:
    pass

# ─────────────── variables globales ─────────────
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]
GIT_SHA = os.getenv("GIT_SHA", "unknown")
APP_START = datetime.datetime.utcnow().isoformat()

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

TEMPLATES: list[Dict[str, Any]] = [
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "oc-lettings-site.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ─────────────── logging ───────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

# ─────────────── Sentry (optionnel) ─────────────
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
            environment=os.getenv("DJANGO_SETTINGS_MODULE", "unknown"),
            send_default_pii=False,
        )
    except ModuleNotFoundError:
        logging.warning("sentry-sdk non installé → Sentry désactivé")

# ─────────────── bannière de démarrage ──────────
print(
    "\n".join(
        [
            "=" * 80,
            f"Mode        : {'PROD' if 'prod' in os.getenv('DJANGO_SETTINGS_MODULE', '') else 'DEV'}",
            f"Git commit  : {GIT_SHA}",
            f"Start (UTC) : {APP_START}",
            f"Templates   : {BASE_DIR / 'templates'}",
            "=" * 80,
        ]
    )
)
