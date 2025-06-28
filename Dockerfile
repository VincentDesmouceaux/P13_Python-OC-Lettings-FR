# syntax=docker/dockerfile:1
# ──────────────────────────────────────────────────────────────
# Image unique ~150 Mo compressée – Python 3.12 + Django 4.2
# ──────────────────────────────────────────────────────────────
FROM python:3.12-slim

# ==== 1. Variables d’environnement ===========================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG=false \            
    WHITENOISE_MANIFEST_STRICT=false \
    PORT=8000

WORKDIR /app                       # racine du code dans l’image

# ==== 2. Dépendances système minimales =======================
RUN apt-get update -qq \
    && apt-get -y --no-install-recommends upgrade \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ==== 3. Dépendances Python ==================================
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ==== 4. Code source  ========================================
COPY . .

# ==== 5. Collecte statique (WhiteNoise) ======================
RUN python manage.py collectstatic --noinput

# ==== 6. Exposition & démarrage ==============================
EXPOSE ${PORT}
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000", "--timeout", "120"]
