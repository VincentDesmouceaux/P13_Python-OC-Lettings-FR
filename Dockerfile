FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    DJANGO_DEBUG=false

WORKDIR /app

# 1) Dépendances système minimales (mise à jour via cache buildkit)
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update -qq && \
    apt-get -y --no-install-recommends upgrade && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) Dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 3) Code
COPY . .

# 4) Collecte statique (pas de manifest → jamais d’erreur)
RUN python manage.py collectstatic --noinput

# 5) Exposition & lancement
EXPOSE ${PORT}
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000"]
