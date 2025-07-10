# ─────────────────────────────────────────────────────────────
# Image d’exécution Django prête pour la prod
# ─────────────────────────────────────────────────────────────
FROM python:3.12-slim-bullseye

LABEL org.opencontainers.image.source="https://github.com/VincentDesmouceaux/P13_Python-OC-Lettings-FR"

# ─── Variables d’environnement par défaut (écrasables à l’exécution) ───
ENV \
    # comportement Python
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # paramètres Django
    DJANGO_DEBUG=false \
    DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0,holiday-homes,.code.run" \
    WHITENOISE_MANIFEST_STRICT=false \
    # port par défaut : sera écrasé par Northflank si PORT est injecté
    PORT=8000

WORKDIR /app

# 1) apt (cache BuildKit)
RUN --mount=type=cache,target=/var/cache/apt \
    set -eux && \
    apt-get update -qq && \
    apt-get -y --no-install-recommends upgrade && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) dépendances Python
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 3) code source
COPY . .

# 4) collectstatic (fichiers statiques prêts pour Whitenoise)
RUN python manage.py collectstatic --noinput

# ─── Port exposé (dynamique) ───
EXPOSE ${PORT}

# ─── Commande de démarrage ───
# Utilise le port injecté (ou 8000 par défaut) sans rebuild d’image.
CMD ["sh", "-c", "gunicorn oc_lettings_site.wsgi:application -b 0.0.0.0:${PORT} --timeout 120"]
