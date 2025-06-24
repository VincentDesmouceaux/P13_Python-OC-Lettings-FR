# ------------------------------------------------------------------
FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.source="https://github.com/vincentdesmouceaux/P13_Python-OC-Lettings-FR"

ARG PORT=8000
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    WHITENOISE_MANIFEST_STRICT=false

WORKDIR /app

# ---- 1. Paquets système (cache APT pour accélérer le CI) ----------
RUN --mount=type=cache,target=/var/cache/apt \
    set -eux; \
    apt-get update -qq && \
    apt-get -y --no-install-recommends upgrade && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ---- 2. Dépendances Python ---------------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ---- 3. Code source ----------------------------------------------
COPY . .

# ---- 4. Collecte statique (strict OFF) ---------------------------
ENV DJANGO_DEBUG=false
RUN python manage.py collectstatic --noinput

EXPOSE ${PORT}
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000"]
