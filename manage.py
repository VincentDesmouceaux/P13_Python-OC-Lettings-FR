#!/usr/bin/env python
"""
manage.py – Point d’entrée de gestion du projet Django
======================================================

Ce script sert de point central pour exécuter toutes les commandes de gestion
de Django comme ``runserver``, ``migrate``, ``createsuperuser``, etc.

Fonctionnement
--------------

1. Définit la variable d’environnement ``DJANGO_SETTINGS_MODULE`` si elle
   n’est pas déjà définie (``oc_lettings_site.settings``).
2. Exécute la commande passée en argument via ``execute_from_command_line`` :

   - ``python manage.py runserver``
   - ``python manage.py migrate``

Utilisation
-----------

Ce script est généralement invoqué depuis le terminal ::

    $ python manage.py <commande>

Exemples ::

    $ python manage.py runserver
    $ python manage.py test
    $ python manage.py collectstatic
"""
import os
import sys


def main() -> None:
    """
    Fonction principale exécutée lorsque le script est lancé directement.
    Elle configure la variable d’environnement DJANGO_SETTINGS_MODULE
    puis exécute la commande Django passée via la ligne de commande.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")
    # Exécute la commande Django (ex. runserver, migrate, etc.)
    from django.core.management import execute_from_command_line  # type: ignore

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
