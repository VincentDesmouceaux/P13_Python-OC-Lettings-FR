Technologies & stack
====================

Back
----

- **Python 3.12**
- **Django 4.2**
- **Gunicorn** (serveur WSGI)
- **WhiteNoise** (fichiers statiques)
- **Sentry** (observabilité / erreurs)

Base de données
---------------

- **SQLite** pour les tests/CI
- **PostgreSQL** recommandé en production

Qualité / CI
------------

- **pytest**, **pytest-cov**
- **flake8** (PEP8), **black** (formatage auto)
- **GitHub Actions** → **Docker Hub** → **Northflank**

Documentation
-------------

- **Sphinx 8.x**
- **Furo** (thème)
- **sphinxcontrib-mermaid** (diagrammes)
