Quickstart (Docker-first)
=========================

Objectif
--------

Lancer l’application **en production containerisée** en 5 commandes, sans installer Python localement.

Les 5 commandes
---------------

::

   # 1) Cloner
   git clone <URL_REPO> && cd P13_Python-OC-Lettings-FR

   # 2) Préparer l’environnement
   cp .env.example .env   # puis adaptez les valeurs si nécessaire

   # 3) (optionnel) Lister les commandes utiles
   make help

   # 4) Build + (re)lance le conteneur
   make rebuild

   # 5) Vérifier que ça tourne
   open http://localhost:8001    # macOS
   # ou : xdg-open http://localhost:8001  # Linux
   # ou : ouvrez votre navigateur et tapez http://localhost:8001

Commandes courantes
-------------------

- **Logs en direct** ::

    make logs

- **Arrêter / supprimer le conteneur** ::

    make stop

- **Appliquer les migrations** ::

    docker exec -it oc-lettings python manage.py migrate

- **Lancer les tests** ::

    docker exec -it oc-lettings pytest -q

- **Collecter les fichiers statiques (prod)** ::

    docker exec -it oc-lettings python manage.py collectstatic --noinput

- **Ouvrir un shell Django** ::

    docker exec -it oc-lettings python manage.py shell

Générer la documentation (hors conteneur)
-----------------------------------------

::

   pip install -r docs/requirements.txt
   make -C docs html
   open docs/build/html/index.html  # Linux : xdg-open

Astuce
------

Tapez ``make help`` à la racine du projet pour afficher la liste des cibles disponibles
(Docker + Docs).
