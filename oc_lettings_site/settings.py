"""
Configuration Django pour l'application OC Lettings

Ce fichier contient tous les paramètres nécessaires au fonctionnement de l'application
dans différents environnements (développement, test, production).

Principales caractéristiques:
──────────────────────────────
• Mode DEV par défaut - passe en PROD quand DJANGO_DEBUG=false
• Gestion des fichiers statiques:
    - DEV: servis depuis <projet>/static/
    - PROD: collectés dans <projet>/staticfiles/ (WhiteNoise + manifest compressé)
• Intégration avec Sentry pour le suivi des erreurs
• Chargement des variables d'environnement depuis un fichier .env
• Configuration sécurisée pour les environnements de production
• Logging configurable
• Support Docker et Northflank
"""

from __future__ import annotations

import datetime
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict

# =======================================================================
# 0. Chargement des variables d'environnement (facultatif)
# =======================================================================
"""
Charge les variables d'environnement depuis un fichier .env situé à la racine du projet.
Utile pour le développement local. En production, les variables doivent être définies
dans l'environnement d'exécution.

Priorité des valeurs:
1. Variables existantes dans l'environnement
2. Variables du fichier .env (si load_dotenv est appelé avec override=True)
"""

BASE_DIR: Path = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv  # type: ignore
    # override=True : les variables du .env *écrasent* l'environnement existant
    load_dotenv(BASE_DIR / ".env", override=True)
except ModuleNotFoundError:
    # Si python-dotenv n'est pas installé, on continue sans
    pass

# =======================================================================
# 1. Contexte d'exécution
# =======================================================================
"""
Détermine le contexte d'exécution de l'application:
- DEBUG: Mode de débogage Django (désactivé en production)
- PROD: Indicateur spécifique pour notre configuration
- RUNSERVER: Si l'application est lancée avec runserver
- RUNNING_TESTS: Si les tests sont en cours d'exécution
"""


def str2bool(val: str) -> bool:
    """Convertit une chaîne en booléen (supporte plusieurs formats)"""
    return val.lower() in {"1", "true", "yes", "y"}


# Détection automatique du mode d'exécution
RUNSERVER = "runserver" in sys.argv
RUNNING_TESTS = "pytest" in sys.argv[0] or "test" in sys.argv

# DEBUG est activé par défaut, sauf si explicitement désactivé
DEBUG: bool = str2bool(os.getenv("DJANGO_DEBUG", "true"))

# PROD est vrai seulement si DEBUG est désactivé ET nous ne sommes pas en train de tester
PROD:  bool = not DEBUG and not RUNNING_TESTS

# =======================================================================
# 2. Sécurité - Clés & Hosts
# =======================================================================
"""
Configuration des paramètres de sécurité critiques:
- SECRET_KEY: Clé secrète pour les signatures cryptographiques
- ALLOWED_HOSTS: Domaines autorisés à servir l'application
- CSRF_TRUSTED_ORIGINS: Origines fiables pour les requêtes CSRF
- Configuration proxy pour les déploiements derrière un reverse proxy
"""

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")

# Liste des hôtes autorisés (séparés par des virgules dans les variables d'env)
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()
]

# Liste des origines de confiance pour CSRF
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

# Configuration pour les déploiements derrière un proxy (ex: Northflank)
if str2bool(os.getenv("DJANGO_BEHIND_PROXY", "false")):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Validation de la configuration en production
if PROD:
    if not CSRF_TRUSTED_ORIGINS:
        raise ValueError(
            "CSRF_TRUSTED_ORIGINS must be set in production! "
            "Define DJANGO_CSRF_TRUSTED_ORIGINS in your environment variables."
        )
    if not ALLOWED_HOSTS:
        raise ValueError(
            "ALLOWED_HOSTS must be set in production! "
            "Set DJANGO_ALLOWED_HOSTS in your environment variables."
        )

# Configuration spéciale pour le mode développement avec runserver
if RUNSERVER and DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

# =======================================================================
# 3. Applications & Middleware
# =======================================================================
"""
Configuration des applications installées et de la pile middleware.

En production:
- Ajoute le middleware WhiteNoise pour servir les fichiers statiques
- Positionné juste après SecurityMiddleware

Structure:
1. Applications Django core
2. Nos applications personnalisées (lettings, profiles)
3. Extensions (django_extensions pour le développement)
"""

INSTALLED_APPS = [
    # Applications personnalisées
    "oc_lettings_site",
    "lettings",
    "profiles",

    # Applications Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Extensions
    "django_extensions"  # Utile pour le développement (shell_plus, etc.)
]

# Pile middleware de base
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware"]

# Ajout de WhiteNoise uniquement en production pour servir les statiques
if PROD:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Middleware supplémentaires
MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuration des URLs et WSGI
ROOT_URLCONF = "oc_lettings_site.urls"
WSGI_APPLICATION = "oc_lettings_site.wsgi.application"

# =======================================================================
# 4. Templates
# =======================================================================
"""
Configuration du système de templates:
- Dossiers de recherche des templates
- Processeurs de contexte
- Options de débogage

Particularités:
- Le dossier 'templates' à la racine du projet est inclus
- Un processeur de contexte personnalisé pour Sentry est ajouté
"""

TEMPLATES: list[Dict[str, Any]] = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],  # Dossier global de templates
    "APP_DIRS": True,  # Recherche des templates dans les apps
    "OPTIONS": {
        "context_processors": [
            # Processeurs standards
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",

            # Processeur personnalisé pour injecter SENTRY_DSN dans les templates
            "oc_lettings_site.context_processors.sentry_dsn",
        ],
    },
}]

# =======================================================================
# 5. Base de données & Internationalisation
# =======================================================================
"""
Configuration de la base de données et des paramètres internationaux.

Actuellement:
- Utilise SQLite comme base par défaut
- Configuration facilement adaptable pour PostgreSQL/MySQL
- Fuseau horaire UTC
- Internationalisation activée
"""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "oc-lettings-site.sqlite3",
    }
}

# Paramètres de langue et fuseau horaire
LANGUAGE_CODE, TIME_ZONE = "en-us", "UTC"
USE_I18N = USE_TZ = True  # Activation de l'internationalisation et du timezone
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # Type de clé par défaut

# =======================================================================
# 6. Fichiers Statiques
# =======================================================================
"""
Gestion des fichiers statiques (CSS, JS, images) :
- En développement: servis directement depuis STATICFILES_DIRS
- En production: collectés dans STATIC_ROOT et servis par WhiteNoise

WhiteNoise configuration:
- Compression des fichiers
- Gestion des manifestes pour le cache-busting
"""

# URL de base pour les fichiers statiques
STATIC_URL = "/static/"

# Dossiers sources pour les fichiers statiques
STATICFILES_DIRS = [BASE_DIR / "static"]

# Dossier de destination pour collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configuration du stockage des fichiers statiques
if PROD:
    # En production: utilisation de WhiteNoise avec compression
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        }
    }
else:
    # En développement: stockage standard
    STORAGES = {
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        }
    }

# =======================================================================
# 7. Logging
# =======================================================================
"""
Configuration du système de logging:
- Niveau de log configurable par variable d'environnement
- Sortie des logs vers la console
- Désactivation possible des loggers existants
"""

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,  # Conserve les loggers existants
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",  # Sortie vers la console
        }
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,  # Niveau global
    },
}

# =======================================================================
# 8. Intégration Sentry (Optionnelle)
# =======================================================================
"""
Configuration de l'intégration avec Sentry pour le suivi des erreurs.

Fonctionnalités:
- Suivi des erreurs Django
- Suivi des logs
- Échantillonnage des performances
- Environnement spécifique (production/développement)
- Release tracking
"""

SENTRY_DSN = os.getenv("SENTRY_DSN")  # Clé DSN de Sentry
SENTRY_RELEASE = os.getenv("SENTRY_RELEASE", "dev")  # Version de l'application

if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[
                DjangoIntegration(),  # Intégration Django
                LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
            ],
            traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE", "0.1")),
            environment="production" if PROD else "development",
            release=SENTRY_RELEASE,  # Version de l'application
            send_default_pii=False,  # Ne pas envoyer d'info personnelle
        )
    except ModuleNotFoundError:
        logging.warning("⚠️  sentry-sdk absent → Sentry désactivé")

# =======================================================================
# 9. Bannière de démarrage
# =======================================================================
"""
Affiche une bannière avec les paramètres clés au démarrage de l'application.
Utile pour le débogage et la confirmation de la configuration.
"""

print("\n".join([
    "=" * 80,
    f"Mode        : {'PROD' if PROD else 'DEV'}",
    f"DEBUG       : {DEBUG}",
    f"Templates   : {BASE_DIR / 'templates'}",
    f"UTC start   : {datetime.datetime.utcnow().isoformat()}",
    "=" * 80,
]))
