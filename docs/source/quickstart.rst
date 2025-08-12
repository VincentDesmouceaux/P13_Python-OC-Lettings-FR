Quickstart – 5 minutes pour tout lancer 🌅
==========================================

Local (prod-like Docker)
------------------------

.. code-block:: bash

   # reconstruire et relancer (prod-like local)
   make rebuild

   # suivre les logs
   make logs

   # arrêter et supprimer le conteneur
   make stop

   # construire seulement
   make build

   # lancer seulement (si déjà buildée)
   make run

Depuis Docker Hub (image distante)
----------------------------------

Définissez `DOCKER_REPO` (et éventuellement `IMAGE_TAG`) dans ``.env`` ou en variable d’environnement :

.. code-block:: bash

   # .env (extrait)
   DOCKER_REPO=vincentdesmouceaux/oc-lettings-site
   IMAGE_TAG=latest  # optionnel (fallback: latest)

.. code-block:: bash

   # récupérer puis lancer l’image distante
   make up-remote

   # ou forcer un pull à chaque run (Docker récent)
   make run-remote-latest

Voir le détail : :doc:`ops/makefile`.
