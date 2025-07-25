Technologies & stack
====================

Backend
-------

- **Python 3.12**
- **Django 4.2**
- **Gunicorn** (serveur WSGI)
- **WhiteNoise** (staticfiles en prod)
- **Sentry** (télémétrie, erreurs)

Base de données
---------------

- **SQLite** en local rapide
- **PostgreSQL** recommandé en production

Qualité / Tests / CI
--------------------

- **pytest** pour les tests
- **flake8** (règles strictes, non modifiables)
- **GitHub Actions** : lint + tests + build Docker + déploiement Northflank
- **Couverture de test > 80 %** (bloquant)

Documentation
-------------

- **Sphinx 8.x**
- **Thème Furo** + **CSS custom** (couleurs “OC sunsets” 🌇)
- **sphinxcontrib-mermaid** pour les diagrammes

Déploiement
-----------

- **Docker** (multi-arch, tags SHA)
- **Northflank** (build & run)
- **Sentry release** publiée à chaque déploiement
