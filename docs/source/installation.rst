Installation
============

Objectif
--------

Démarrer **tout en conteneur**, sans installer Python ni les dépendances en local.
Le développement « local » se fait en lançant l’image Docker et en pilotant
l’application via les commandes du ``Makefile``.

Prérequis
---------

- Docker 24+ (Desktop ou Engine)
- GNU Make
- (Optionnel) ``envsubst`` si tu veux templater ton ``.env``

Étapes rapides
--------------

1. **Cloner le dépôt** ::

      git clone <URL_REPO>
      cd P13_Python-OC-Lettings-FR

2. **Préparer l’environnement**  
   Copie ``.env.example`` vers ``.env`` et ajuste les valeurs (voir :doc:`../ops/settings`).

3. **(One-liner) Build + run** ::

      make rebuild

   Cela effectue :
   - ``docker build`` de l’image ;
   - arrêt/suppression du conteneur s’il existe ;
   - relance du conteneur sur ``http://localhost:8000``.

4. **Consulter les logs** (stream) ::

      make logs

5. **Arrêter / supprimer le conteneur** ::

      make stop

Commandes utiles dans le conteneur
----------------------------------

- **Appliquer les migrations** ::

    docker exec -it oc-lettings python manage.py migrate

- **Lancer les tests** ::

    docker exec -it oc-lettings pytest -q

- **Collecter les fichiers statiques (prod)** ::

    docker exec -it oc-lettings python manage.py collectstatic --noinput

- **Ouvrir un shell Django** ::

    docker exec -it oc-lettings python manage.py shell

Cycle de dev le plus courant
----------------------------

1. Modifie le code.
2. **Reconstruis et relance** ::

      make rebuild

3. Regarde les **logs** ::

      make logs

4. Accède à l’app : ``http://localhost:8000``.

Alternative : démarrer sans Docker
----------------------------------

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver


Documentation (Sphinx)
----------------------

La doc est générée **depuis ta machine hôte** (plus simple et rapide) :

::

   pip install -r docs/requirements.txt
   make -C docs html
   open docs/build/html/index.html  # macOS (Linux : xdg-open)

Astuce : exécute ``make help`` à la racine du projet pour lister toutes les cibles
disponibles (Docker + Docs).
