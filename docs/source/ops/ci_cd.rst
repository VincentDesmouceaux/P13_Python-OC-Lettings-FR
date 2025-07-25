CI / CD (GitHub Actions)
========================

Objectifs
---------

- Lancer automatiquement **tests**, **lint** et **build de la doc** à chaque PR.
- Déployer automatiquement sur l’environnement cible après merge sur ``main``.

Pipeline type
-------------

1. **Install** deps
2. **Lint** (flake8, black --check, isort --check-only)
3. **Tests** (pytest + couverture)
4. **Build Sphinx** (sans warnings bloquants en prod)
5. **Déploiement** (Render/Heroku/Docker registry)

Exemple (pseudo YAML)
---------------------

.. code-block:: yaml

   name: CI

   on:
     pull_request:
     push:
       branches: [ main ]

   jobs:
     tests:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.12"
         - run: pip install -r requirements.txt
         - run: pytest --maxfail=1 --disable-warnings -q

     docs:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.12"
         - run: pip install -r docs/requirements.txt
         - run: make -C docs html

Stratégie de versionnement
--------------------------

- Utiliser une variable ``SENTRY_RELEASE`` ou un tag Git pour versionner :
  - artefacts CI
  - déploiement
  - Sentry releases
