FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.source="https://github.com/VincentDesmouceaux/P13_Python-OC-Lettings-FR"

# ——————————————————— ENV
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_DEBUG=false \
    WHITENOISE_MANIFEST_STRICT=false

WORKDIR /app

# 1) dépendances système (cachées)
RUN --mount=type=cache,target=/var/cache/apt \
    set -eux && \
    apt-get update -qq && apt-get -y --no-install-recommends upgrade && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 3) code source
COPY . .

# 4) collecte statique
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000", "--timeout", "120"]
