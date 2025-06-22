FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

WORKDIR /app

# --------------------------------------------------------------------
# 1) Mises à jour sécurité Debian
RUN set -eux; \
    apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------
# 2) Dépendances Python (inclut désormais WhiteNoise)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# --------------------------------------------------------------------
# 3) Code source
COPY . .

# --------------------------------------------------------------------
# 4) Collecte des fichiers statiques (mode PROD)
ENV DJANGO_DEBUG=false
RUN python manage.py collectstatic --noinput

# --------------------------------------------------------------------
# 5) Exposition du port + CMD
EXPOSE ${PORT}
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000"]
