# ────────────────────────────────────────────────────────────────
# Image unique ~150 Mo (compressée) pour Django 4.2 / Python 3.12
# ────────────────────────────────────────────────────────────────
FROM python:3.12-slim-bookworm

LABEL org.opencontainers.image.source="https://github.com/vincentdesmouceaux/P13_Python-OC-Lettings-FR"

ARG PORT=8000                 # PORT en dur dans l’image pour EXPOSE
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WHITENOISE_MANIFEST_STRICT=false  

WORKDIR /app

# ─────────────── 1. dépendances système (cache APT) ─────────────
RUN --mount=type=cache,target=/var/cache/apt \
    set -eux; \
    apt-get update -qq; \
    apt-get -y --no-install-recommends upgrade; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

# ─────────────── 2. dépendances Python ──────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ─────────────── 3. code applicatif ─────────────────────────────
COPY . .

# ─────────────── 4. collectstatic (DJANGO_DEBUG=false) ──────────
# On force DEBUG=false UNIQUEMENT pour collectstatic.
RUN DJANGO_DEBUG=false python manage.py collectstatic --noinput

# ─────────────── 5. exécution Gunicorn ──────────────────────────
EXPOSE ${PORT}
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000", "--timeout", "120"]
