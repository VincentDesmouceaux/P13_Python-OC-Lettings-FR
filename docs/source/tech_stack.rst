Technologies & stack
====================

Backend
-------

- **Python** 3.12
- **Django** 4.2
- **Gunicorn** (prod)
- **WhiteNoise** pour les fichiers statiques
- **Sentry** pour la télémétrie (logs/erreurs)

Base de données
---------------

- **SQLite** en dev
- **PostgreSQL** en prod (recommandé)

Qualité / Tests / CI
--------------------

- **pytest** pour les tests
- **flake8 / black / isort** (optionnel) pour la qualité
- **GitHub Actions** pour CI/CD (voir :doc:`ops/ci_cd`)

Documentation
-------------

- **Sphinx** 8.x
- **Furo** comme thème
- **sphinxcontrib-mermaid** pour les diagrammes

Déploiement
-----------

- **Render / Heroku / Railway** (selon vos choix)
- **Docker** (optionnel) pour build reproductible
