# Dockerfile ────────────────────────────────────────────────────────────────
FROM python:3.12-slim

# 1. Variables d’environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=oc_lettings_site.settings \
    PORT=8000

# 2. Création de l’utilisateur non-root et dossier appli
RUN adduser --disabled-password --gecos "" appuser \
    && mkdir /app \
    && chown appuser:appuser /app

WORKDIR /app                     # on reste root pour l’install

# 3. Dépendances
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 4. Code source
COPY . .

# 5. Fichiers statiques
RUN mkdir -p /app/staticfiles && \
    python manage.py collectstatic --noinput

# 6. On passe en user non-root **seulement maintenant**
USER appuser

EXPOSE $PORT
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "-b", "0.0.0.0:8000"]
