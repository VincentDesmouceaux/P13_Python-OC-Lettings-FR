Installation
============

Objectif
--------

Démarrer **tout en conteneur**, sans installer Python ni les dépendances en local.

Prérequis
---------

- Docker 24+ (Desktop ou Engine)
- GNU Make
- (Optionnel) un fichier ``.env`` pour tes variables

Étapes rapides
--------------

1) **Cloner le dépôt** ::

   git clone <URL_REPO>
   cd P13_Python-OC-Lettings-FR

2) **Préparer l’environnement** ::

   cp .env.example .env
   # personnalise si besoin : PORT, DOCKER_REPO, IMAGE_TAG, SENTRY_DSN, etc.

3) **Build + run (local)** ::

   make rebuild

4) **Vérifier** : http://localhost:8000

Commandes utiles (dans le conteneur)
------------------------------------

- **Migrations** ::

    docker exec -it oc-lettings python manage.py migrate

- **Tests** ::

    docker exec -it oc-lettings pytest -q

- **Collecte des statiques (prod)** ::

    docker exec -it oc-lettings python manage.py collectstatic --noinput

- **Shell Django** ::

    docker exec -it oc-lettings python manage.py shell

Alternative : démarrer sans Docker
----------------------------------

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # Windows : venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
