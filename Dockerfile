# Dockerfile
FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.source="https://github.com/VincentDesmouceaux/P13_Python-OC-Lettings-FR"

# ─────────── Variables d’environnement de base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_DEBUG=false \         
    WHITENOISE_MANIFEST_STRICT=false

# ─────────── Dossier applicatif
WORKDIR /app

# 1) Dépendances système
RUN --mount=type=cache,target=/var/cache/apt \
    set -eux && \
    apt-get update -qq && apt-get -y --no-install-recommends upgrade && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) Dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 3) Code source
COPY . .

# 4) Collecte statique (avec backend « relaxed »)
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000", "--timeout", "120"]
