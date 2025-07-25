Quickstart
==========

Démarrage en 60 secondes
------------------------

1. Cloner le repo, créer un venv, installer les deps.
2. Lancer la base (SQLite par défaut) et les migrations.
3. Démarrer le serveur de dev.
4. Ouvrir http://127.0.0.1:8000.

Commandes utiles
----------------

- **Lancer le serveur** ::

    python manage.py runserver

- **Lancer les tests** ::

    pytest

- **Créer un superuser** ::

    python manage.py createsuperuser

- **Collecter les fichiers statiques** (prod) ::

    python manage.py collectstatic --noinput
