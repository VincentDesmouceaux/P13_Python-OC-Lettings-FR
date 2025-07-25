Quickstart – 5 minutes pour tout lancer 🌅
==========================================


Local = **Docker en mode prod-like**. Pas d’environnement “dev” séparé :  
on **reconstruit & (re)lance** le conteneur avec les variables d’env de prod.

Commandes utiles (Makefile)
---------------------------

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

Voir le détail : :doc:`ops/makefile`.

Afficher la doc localement
--------------------------

.. code-block:: bash

   pip install -r docs/requirements.txt
   make -C docs html
   open docs/build/html/index.html  # macOS (Linux: xdg-open)

Ce que vous obtenez après ce Quickstart
---------------------------------------

- Le site tourne en **Gunicorn + WhiteNoise** (comme en prod).
- Vous pouvez **naviguer**, **tester l’admin**, **vérifier les logs**, **simuler des erreurs** (Sentry).
- Vous pouvez **modifier n’importe quel fichier**, `make rebuild` et **revalider la prod locale**.
