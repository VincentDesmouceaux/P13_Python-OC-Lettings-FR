Déploiement (prod)
==================

Checklist
---------

- ``DJANGO_DEBUG=False``
- ``DJANGO_SECRET_KEY`` défini
- ``DJANGO_ALLOWED_HOSTS`` et ``DJANGO_CSRF_TRUSTED_ORIGINS`` réglés
- **Migrations** appliquées
- **collectstatic** exécuté
- **SENTRY_DSN** présent (optionnel, recommandé)

Commande de démarrage (conteneur)
---------------------------------

Gunicorn (via `CMD` du Dockerfile) ::

  gunicorn oc_lettings_site.wsgi:application -b 0.0.0.0:${PORT} --timeout 120

Northflank
----------

- Récupère l’image depuis Docker Hub
- Injecte les variables d’environnement
- Expose l’URL publique (type ``*.code.run``)
