Déploiement
===========

Checklist pré-prod
------------------

- ``DJANGO_DEBUG = false``
- ``SECRET_KEY`` défini
- ``ALLOWED_HOSTS`` / ``CSRF_TRUSTED_ORIGINS`` configurés
- **Migrations appliquées**
- **collectstatic exécuté**
- **Sentry activé (optionnel mais recommandé)**

Procédure “manuelle” (référence)
--------------------------------

1. **Build image**  
   ``docker build --build-arg GIT_SHA=$(git rev-parse HEAD) -t $DOCKER_REPO:$TAG .``

2. **Push**  
   ``docker push $DOCKER_REPO:$TAG``

3. **Migrations**  
   ``python manage.py migrate`` (via job/run sur la plateforme)

4. **Collectstatic**  
   ``python manage.py collectstatic --noinput``

5. **Run Gunicorn**  
   ``gunicorn oc_lettings_site.wsgi:application -b 0.0.0.0:8000``

Healthchecks & rollback
-----------------------

- Endpoint **/health** (à ajouter si besoin).
- Historiser les images (tag SHA) pour rollback rapide.
