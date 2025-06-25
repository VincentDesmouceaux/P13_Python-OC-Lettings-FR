# ───────── base ─────────
FROM python:3.12-slim-bookworm AS base
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ───────── dev ──────────
FROM base AS dev
ENV DJANGO_SETTINGS_MODULE=oc_lettings_site.settings.dev
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ───────── prod ─────────
FROM base AS prod
ARG PORT=8000
ARG GIT_SHA=unknown
ENV \
    DJANGO_SETTINGS_MODULE=oc_lettings_site.settings.prod \
    PORT=$PORT \
    GIT_SHA=$GIT_SHA \
    WHITENOISE_MANIFEST_STRICT=false

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE ${PORT}
CMD ["sh", "-c", "gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120 --log-level info"]
