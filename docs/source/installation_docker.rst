Installation (Docker-first)
===========================

Prérequis
---------

- Docker 24+
- GNU Make

Étapes
------

1. **Cloner le dépôt** ::

      git clone <URL_REPO>
      cd P13_Python-OC-Lettings-FR

2. **Configurer les variables d’environnement** ::

      cp .env.example .env
      # Adapter les valeurs (voir :doc:`ops/settings`)

3. **Build + run (en une commande)** ::

      make rebuild

4. **Vérifier** : http://localhost:8000

Commandes utiles
----------------

- **Logs** ::

    make logs

- **Arrêter / supprimer** ::

    make stop

- **Migrations** ::

    docker exec -it oc-lettings python manage.py migrate

- **Tests** ::

    docker exec -it oc-lettings pytest -q

Documentation Sphinx
--------------------

::

   pip install -r docs/requirements.txt
   make -C docs html
   open docs/build/html/index.html
