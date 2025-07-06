# ──────────────────────────────────────────────────────────────────────────────
# Image d’exécution Django prête pour la prod
# ──────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.source="https://github.com/VincentDesmouceaux/P13_Python-OC-Lettings-FR"

# ───── Variables d’environnement par défaut (surchargées à l’exécution) ─────
# • DJANGO_ALLOWED_HOSTS reçoit ici un placeholder pour que `collectstatic`
#   puisse tourner pendant le build ; en prod tu l’écrases dans Northflank.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_DEBUG=false \
    DJANGO_ALLOWED_HOSTS=localhost,0.0.0.0 \
    WHITENOISE_MANIFEST_STRICT=false

WORKDIR /app

# ───── 1) dépendances système (cachées via le cache BuildKit) ────────────────
RUN --mount=type=cache,target=/var/cache/apt \
    set -eux && \
    apt-get update -qq && \
    apt-get -y --no-install-recommends upgrade && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ───── 2) dépendances Python ────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ───── 3) code applicatif ───────────────────────────────────────────────────
COPY . .

# ───── 4) statiques collectés (placeholder ALLOWED_HOSTS déjà présent) ─────
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000", "--timeout", "120"]
