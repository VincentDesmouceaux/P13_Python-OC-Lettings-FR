Déploiement
===========

Checklist pré‑prod
------------------

- ``DEBUG=False``
- ``ALLOWED_HOSTS`` configuré
- ``SECRET_KEY`` secret
- ``SENTRY_DSN`` configuré (optionnel)
- **Migrations** appliquées
- **collectstatic** exécuté

Procédure générique
-------------------

1. **Build** (Docker ou installation simple)
2. **Migrations** ::

     python manage.py migrate

3. **Collectstatic** ::

     python manage.py collectstatic --noinput

4. **Démarrer Gunicorn** ::

     gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000

5. (Optionnel) **Reverse proxy** (nginx) devant Gunicorn

Healthchecks & rollback
-----------------------

- Prévoir un endpoint de **healthcheck** (ex : ``/health``).
- Conserver les **migrations versionnées** pour rollback rapide.
