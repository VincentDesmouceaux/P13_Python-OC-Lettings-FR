# ---------- Étape unique (image ~150 Mo compressés) -------------
FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.source="https://github.com/vincentdesmouceaux/P13_Python-OC-Lettings-FR"

ARG PORT=8000
# Strict désactivé pour « collectstatic » (pas de crash si asset manquant)
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    WHITENOISE_MANIFEST_STRICT=false \
    DJANGO_DEBUG=false

WORKDIR /app

# 1) dépendances système – cache APT conservé pendant le build GitHub Actions
RUN --mount=type=cache,target=/var/cache/apt \
    set -eux; \
    apt-get update -qq && \
    apt-get -y --no-install-recommends upgrade && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 3) code source
COPY . .

# 4) collecte statique (WhiteNoise « relaxed »)
RUN python manage.py collectstatic --noinput

# 5) exécution
EXPOSE ${PORT}
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000", "--timeout", "120"]
