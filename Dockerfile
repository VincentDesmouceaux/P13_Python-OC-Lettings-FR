# ─────────────────────────────────────────────────────────────
# Image d’exécution Django prête pour la prod
# ─────────────────────────────────────────────────────────────
#
# Description:
# Cette image Docker est optimisée pour l'exécution en production de l'application Django Lettings.
# 
# Caractéristiques:
# - Base légère (Python 3.12 sur Debian Bullseye slim)
# - Configuration sécurisée par défaut
# - Gestion des dépendances Python
# - Collecte des fichiers statiques
# - Intégration avec Sentry pour le suivi des erreurs
# - Configuration dynamique via variables d'environnement
#
# Variables d'environnement configurables:
# • SENTRY_RELEASE: Identifiant de release pour Sentry (défaut: SHA du commit)
# • PYTHONUNBUFFERED: Désactive le buffering des sorties Python (1=activé)
# • PYTHONDONTWRITEBYTECODE: Empêche la création de fichiers .pyc (1=activé)
# • DJANGO_DEBUG: Mode debug Django (false=production)
# • DJANGO_ALLOWED_HOSTS: Hôtes autorisés (séparés par des virgules)
# • DJANGO_CSRF_TRUSTED_ORIGINS: Origines CSRF fiables
# • WHITENOISE_MANIFEST_STRICT: Comportement strict pour les manifestes (false)
# • PORT: Port d'écoute du serveur (défaut: 8000)
#
# Utilisation:
# 1. Construire l'image:
#    docker build --build-arg GIT_SHA=$(git rev-parse HEAD) -t lettings:prod .
#
# 2. Exécuter le conteneur:
#    docker run -p 8000:8000 -e DJANGO_SECRET_KEY=secret lettings:prod
# ─────────────────────────────────────────────────────────────

FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.source="https://github.com/VincentDesmouceaux/P13_Python-OC-Lettings-FR"

# ─────────────────────────────────────────────────────────────
# 0) SHA du commit : injecté depuis le workflow
#
# Argument de build:
# • GIT_SHA: SHA du commit Git pour le suivi des déploiements
#   - Valeur par défaut: 'dev'
#   - Doit être fourni lors du build via `--build-arg GIT_SHA=<commit_sha>`
# ─────────────────────────────────────────────────────────────
ARG GIT_SHA=dev

# ─────────────────────────────────────────────────────────────
# Variables d’environnement par défaut (écrasables à l’exécution)
#
# Description:
# • SENTRY_RELEASE: Utilisé par le SDK Sentry pour identifier la version déployée
# • PYTHON*: Optimise le comportement de Python en environnement conteneurisé
# • DJANGO_DEBUG: DÉSACTIVÉ en production pour la sécurité
# • DJANGO_ALLOWED_HOSTS: Domaines autorisés à servir l'application
# • DJANGO_CSRF_TRUSTED_ORIGINS: Origines autorisées pour les requêtes CSRF
# • WHITENOISE_MANIFEST_STRICT: Désactivé pour éviter des erreurs en production
# • PORT: Port interne d'écoute du serveur Gunicorn
# ─────────────────────────────────────────────────────────────
ENV \
    # propagation de la release à Sentry
    SENTRY_RELEASE=${GIT_SHA} \
    # comportement Python
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # paramètres Django
    DJANGO_DEBUG=false \
    DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0,holiday-homes,.code.run" \
    DJANGO_CSRF_TRUSTED_ORIGINS="https://*.code.run" \
    WHITENOISE_MANIFEST_STRICT=false \
    # port par défaut : sera écrasé par Northflank si PORT est injecté
    PORT=8000

# Définit le répertoire de travail dans le conteneur (/app)
WORKDIR /app

# ─────────────────────────────────────────────────────────────
# 1) Mise à jour du système avec cache BuildKit
#
# Description:
# - Utilise le cache BuildKit pour accélérer les builds ultérieurs
# - Met à jour les paquets système existants
# - Nettoie les caches pour réduire la taille de l'image
# ─────────────────────────────────────────────────────────────
RUN --mount=type=cache,target=/var/cache/apt \
    set -eux && \
    apt-get update -qq && \
    apt-get -y --no-install-recommends upgrade && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────────────────────
# 2) Installation des dépendances Python
#
# Étapes:
# 1. Copie du fichier requirements.txt dans l'image
# 2. Mise à jour de pip
# 3. Installation des paquets sans cache pour réduire la taille
# ─────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────
# 3) Copie du code source
#
# Description:
# Copie de l'ensemble du code source dans le répertoire /app du conteneur
# ─────────────────────────────────────────────────────────────
COPY . .

# ─────────────────────────────────────────────────────────────
# 4) Préparation des fichiers statiques pour Whitenoise
#
# Description:
# - Collecte tous les fichiers statiques dans le répertoire staticfiles
# - Nécessaire pour le bon fonctionnement de Whitenoise
# - Option --noinput: exécution non interactive
# ─────────────────────────────────────────────────────────────
RUN python manage.py collectstatic --noinput

# ─────────────────────────────────────────────────────────────
# Exposition du port (dynamique)
#
# Description:
# Expose le port spécifié par la variable d'environnement PORT
# ─────────────────────────────────────────────────────────────
EXPOSE ${PORT}

# ─────────────────────────────────────────────────────────────
# Commande de démarrage
#
# Description:
# - Lance le serveur Gunicorn
# - Écoute sur toutes les interfaces (0.0.0.0) au port configuré
# - Timeout de 120 secondes pour les workers
# - Utilise le module WSGI de l'application Django
# ─────────────────────────────────────────────────────────────
CMD ["sh", "-c", "gunicorn oc_lettings_site.wsgi:application -b 0.0.0.0:${PORT} --timeout 120"]