# ────────────────────────────────────────────────────────────────
FROM python:3.12-slim-bullseye

# Update system packages to address vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

WORKDIR /app

# 1. Dépendances
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 2. Code
COPY . .

# 3. Collecte statique **uniquement** à l’image (DJANGO_DEBUG=false implicite)
ENV DJANGO_DEBUG=false
RUN python manage.py collectstatic --noinput

EXPOSE ${PORT}

# 4. Démarrage (gunicorn → prod)
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000"]
