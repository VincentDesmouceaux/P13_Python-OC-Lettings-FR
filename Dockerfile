# ─────────────────────────────────────────────────────────────
# Image d’exécution Django prête pour la production
# ─────────────────────────────────────────────────────────────
#
# Application : OC Lettings
#
# Caractéristiques :
# - Python 3.12
# - Debian Bullseye slim
# - Django + Gunicorn
# - WhiteNoise pour les fichiers statiques
# - Sentry pour le suivi des erreurs
# - Configuration via variables d'environnement
# ─────────────────────────────────────────────────────────────

FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.source="https://github.com/VincentDesmouceaux/P13_Python-OC-Lettings-FR"

# ─────────────────────────────────────────────────────────────
# 0) SHA du commit
# ─────────────────────────────────────────────────────────────

ARG GIT_SHA=dev

# ─────────────────────────────────────────────────────────────
# 1) Variables d'environnement
# ─────────────────────────────────────────────────────────────

ENV SENTRY_RELEASE=${GIT_SHA} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_DEBUG=false \
    DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0,holiday-homes,.code.run" \
    DJANGO_CSRF_TRUSTED_ORIGINS="https://*.code.run" \
    WHITENOISE_MANIFEST_STRICT=false \
    PORT=8000

# ─────────────────────────────────────────────────────────────
# 2) Répertoire de travail
# ─────────────────────────────────────────────────────────────

WORKDIR /app

# ─────────────────────────────────────────────────────────────
# 3) Dépendances Python
#
# Aucun apt-get upgrade :
# les correctifs système proviennent de l'image Python de base.
# ─────────────────────────────────────────────────────────────

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────
# 4) Copie du code source
# ─────────────────────────────────────────────────────────────

COPY . .

# ─────────────────────────────────────────────────────────────
# 5) Fichiers statiques Django / WhiteNoise
# ─────────────────────────────────────────────────────────────

RUN python manage.py collectstatic --noinput

# ─────────────────────────────────────────────────────────────
# 6) Port
# ─────────────────────────────────────────────────────────────

EXPOSE 8000

# ─────────────────────────────────────────────────────────────
# 7) Démarrage Gunicorn
# ─────────────────────────────────────────────────────────────

CMD ["sh", "-c", "gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT} --timeout 120"]
