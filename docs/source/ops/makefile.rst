Makefile (Docker & Docs)
========================

But
---

Fournir des **raccourcis sûrs** pour builder/lancer en local, et **tirer** puis lancer l’image du **Docker Hub** — **sans secrets en dur**.

Chargement du ``.env``
----------------------

- Le Makefile lit les clés (ex: ``PORT``, ``DOCKER_REPO``, ``IMAGE_TAG``) depuis ``.env`` **si présent**.
- Avant un ``docker run``, il crée un ``.env.sanitized`` (ne garde que ``KEY=VALUE`` et commentaires) pour éviter que des lignes décoratives ne cassent l’option ``--env-file``.

Variables utiles
----------------

- ``PORT`` : port hôte (défaut : ``8000``).
- ``DOCKER_REPO`` : image distante (ex. ``vincentdesmouceaux/oc-lettings-site``).
- ``IMAGE_TAG`` : tag distant (ex. ``latest``). *Optionnel* (fallback : ``latest``).
- ``IMAGE`` / ``CONTAINER`` : noms locaux (défaut : ``oc-lettings``).

Cibles disponibles
------------------

- ``make build``  
  Construit l’image **locale** ``oc-lettings``.  
  Si ``DOCKER_REPO`` est défini, tague aussi ``$DOCKER_REPO:$IMAGE_TAG`` (ou ``latest``).

- ``make run``  
  Lance le conteneur **local** en détaché ; port ``$PORT:8000`` ; charge ``.env.sanitized`` si présent.

- ``make stop``  
  Arrête et supprime le conteneur s’il existe (idempotent).

- ``make rebuild``  
  **build → stop → run** (équiv. à “rebuild and restart”).

- ``make logs``  
  Affiche les logs en continu (``Ctrl-C`` pour sortir).

- ``make pull``  
  **Pull l’image distante** (nécessite ``DOCKER_REPO``).

- ``make run-remote``  
  Lance **depuis l’image distante** (utilise ``.env.sanitized`` si présent).

- ``make up-remote``  
  **stop → pull → run-remote** (pull + run en un coup).

- ``make run-remote-latest``  
  Force un pull à chaque exécution (``docker run --pull=always``).

Exemples
--------

**Local (prod-like)** :

.. code-block:: bash

   make rebuild
   make logs
   make stop

**Depuis Docker Hub** :

.. code-block:: bash

   # .env
   DOCKER_REPO=vincentdesmouceaux/oc-lettings-site
   IMAGE_TAG=latest   # optionnel

   make up-remote
   # ou
   make run-remote-latest

Docs (Sphinx)
-------------

.. code-block:: bash

   make -C docs html        # build HTML
   make -C docs serve       # serveur de prévisualisation (si configuré)
   make -C docs clean       # nettoyer build
   make -C docs linkcheck   # vérifier les liens
   make -C docs doctest     # exécuter doctests

.. note::

   Ne commitez jamais votre ``.env`` réel.
   Versionnez **.env.example** et remplissez les valeurs côté CI/CD (secrets GitHub) ou localement.
