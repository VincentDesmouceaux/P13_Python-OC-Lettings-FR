CI / CD (GitHub Actions → Docker → Northflank)
==============================================

Pipeline (vue d’ensemble)
-------------------------

1. **Tests & Lint (flake8 + pytest, cov > 80 %)**  
2. **Build multi-arch & push Docker Hub** (tags : dernier SHA + tag lisible)  
3. **Release Sentry** (versionnée par SHA)  
4. **Déploiement Northflank** (trigger via API)

Règles de déclenchement
-----------------------

- **Branches ≠ master/main** → *tests + lint seulement*
- **master/main** → *tests + lint* ➜ *build & push Docker* ➜ *deploy Northflank*

Docker
------

- **Image prod-ready** (Gunicorn, collectstatic).
- **Taggée par SHA** pour être traçable (Sentry inclut la release dans les events).
- **Tirable localement** :

  .. code-block:: bash

     docker pull $DOCKER_REPO:<sha>
     docker run -p 8000:8000 $DOCKER_REPO:<sha>

Sentry
------

- Publication automatique d’une **release**.
- **SENTRY_RELEASE = SHA** pour faire correspondre les erreurs à une version.

Northflank
----------

- Le job **deploy** appelle l’API Northflank pour **rebuild & redéployer** le service.
- L’URL finale est rappelée en log (``...code.run``).
