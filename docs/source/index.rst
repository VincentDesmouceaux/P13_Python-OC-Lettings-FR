P13 Python OC Lettings — Docs
=============================

Documentation courte, orientée **exploitation** :

- tout tourne en **conteneur Docker** en local (prod-like) ;
- le **CI/CD** est piloté par **GitHub Actions** → **Docker Hub** → **Northflank** ;
- **Sentry** remonte les erreurs en prod.

.. toctree::
   :maxdepth: 1
   :caption: Démarrer

   quickstart
   tech_stack

.. toctree::
   :maxdepth: 1
   :caption: Ops

   ops/ci_cd
   ops/settings
   ops/deployment
   ops/monitoring
   ops/makefile

.. toctree::
   :maxdepth: 1
   :caption: Modèle & URLs

   database
   guides/usage
