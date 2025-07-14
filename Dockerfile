###############################################################################
# Dockerfile ― « oc-lettings »
# ─────────────────────────────────────────────────────────────────────────────
# • Objectif : image minimale de production pour l’application Django
#   « Orange County Lettings ».
# • Base : python:3.12-slim-bullseye  ➜ Debian Bullseye + CPython 3.12
# • Fonctionnalités :
#     ─ Variable SENTRY_RELEASE injectée à la build pour faire le lien avec
#       les releases Sentry créées par GitHub Actions.
#     ─ BuildKit + cache APT pour accélérer les reconstructions locales/CI.
#     ─ Collection des fichiers statiques (‘collectstatic’) prête pour
#       WhiteNoise (aucun serveur web externe requis).
# • Usage :
#     $ docker build -t oc-lettings --build-arg GIT_SHA=$(git rev-parse HEAD) .
#     $ docker run -p 8000:8000 oc-lettings
###############################################################################

# syntax=docker/dockerfile:1.7

# ─────────────────────────────────────────────────────────────
# 0. Image de base
# ─────────────────────────────────────────────────────────────
FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.description="Orange County Lettings – Django production image"
LABEL org.opencontainers.image.source="https://github.com/VincentDesmouceaux/P13_Python-OC-Lettings-FR"

# ─────────────────────────────────────────────────────────────
# 1. Variables build-time & run-time
# ─────────────────────────────────────────────────────────────
# GIT_SHA est passé par le workflow GitHub Actions pour relier l’image à
# la release Sentry (≃ ${{ github.sha }}).  Valeur « dev » en local.
ARG GIT_SHA=dev

# Les variables suivantes peuvent toujours être **surchargées** via
# Northflank / `docker run -e …` ; elles servent seulement de valeurs par
# défaut sûres.
ENV \
    # —— Observabilité ——
    SENTRY_RELEASE=${GIT_SHA} \           
    # —— Comportement Python ——
    # stdout/stderr non bufferisés
    PYTHONUNBUFFERED=1 \
    # pas de fichiers .pyc
    PYTHONDONTWRITEBYTECODE=1 \
    # —— Paramètres Django ——
    DJANGO_DEBUG=false \                  
    DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0,holiday-homes,.code.run" \
    DJANGO_CSRF_TRUSTED_ORIGINS="https://*.code.run" \
    WHITENOISE_MANIFEST_STRICT=false \    
    # —— Infra ——
    PORT=8000

# ─────────────────────────────────────────────────────────────
# 2. Dossier de travail
# ─────────────────────────────────────────────────────────────
WORKDIR /app

# ─────────────────────────────────────────────────────────────
# 3. Système : mises à jour de sécurité + cache APT
# ─────────────────────────────────────────────────────────────
# • `--mount=type=cache,target=/var/cache/apt` ⇒ accélère les rebuilds locaux
# • `set -eux`  ⇒  -e = exit on error, -u = undefined var, -x = echo commands
RUN --mount=type=cache,target=/var/cache/apt \
    set -eux && \
    apt-get update -qq && \
    apt-get -y --no-install-recommends upgrade && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────────────────────
# 4. Dépendances Python
# ─────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────
# 5. Code source de l’application
# ─────────────────────────────────────────────────────────────
COPY . .

# ─────────────────────────────────────────────────────────────
# 6. Collecte des fichiers statiques (WhiteNoise)
# ─────────────────────────────────────────────────────────────
#   → Les assets se retrouvent dans /app/staticfiles/
RUN python manage.py collectstatic --noinput

# ─────────────────────────────────────────────────────────────
# 7. Port exposé (variable)
# ─────────────────────────────────────────────────────────────
EXPOSE ${PORT}

# ─────────────────────────────────────────────────────────────
# 8. Commande de démarrage
# ─────────────────────────────────────────────────────────────
# * `${PORT}` reste dynamique (Northflank peut l’injecter).
# * `--timeout 120` : évite les workers bloqués trop longtemps.
CMD ["sh", "-c", "gunicorn oc_lettings_site.wsgi:application -b 0.0.0.0:${PORT} --timeout 120"]
