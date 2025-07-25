Quickstart (prod-like en local)
===============================

Objectif : lancer l’app **dans un conteneur Docker** (configuration la plus proche de la prod).

Étapes
------

1. **Cloner** le dépôt ::

     git clone <URL_REPO> && cd P13_Python-OC-Lettings-FR

2. **Configurer l’environnement** (copie et ajuste) ::

     cp .env.example .env

3. **Build + run** (en une commande) ::

     make rebuild

4. **Ouvrir l’app** : http://localhost:8000

Commandes utiles (Makefile)
---------------------------

- **Reconstruire et relancer** ::

    make rebuild

- **Voir les logs** ::

    make logs

- **Arrêter et supprimer le conteneur** ::

    make stop

- **(Optionnel) Lancer les tests en local (hors CI)** ::

    docker run --rm oc-lettings pytest -q
