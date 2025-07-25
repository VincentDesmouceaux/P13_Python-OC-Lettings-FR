Interfaces (API / URLs)
=======================

Vue d’ensemble
--------------

L’application expose **des routes HTML classiques** (non REST).  
Si vous exposez une API REST par la suite, documentez-la ici.

Résumé
------

+---------------------+---------------------------+-------------------------------+
| Domaine             | URL                       | Description                   |
+=====================+===========================+===============================+
| Accueil             | ``/``                     | Page d’accueil                |
+---------------------+---------------------------+-------------------------------+
| Lettings (liste)    | ``/lettings/``            | Liste des locations           |
+---------------------+---------------------------+-------------------------------+
| Letting (détail)    | ``/lettings/<id>/``       | Détail d’une location         |
+---------------------+---------------------------+-------------------------------+
| Profiles (liste)    | ``/profiles/``            | Liste des profils             |
+---------------------+---------------------------+-------------------------------+
| Profile (détail)    | ``/profiles/<username>/`` | Détail d’un profil utilisateur|
+---------------------+---------------------------+-------------------------------+

Schéma d’URL (exemple)
----------------------

.. code-block:: text

   /
   ├── lettings/
   │   └── <id>/
   └── profiles/
       └── <username>/
