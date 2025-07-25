Interfaces (API / URLs)
=======================

Vue d’ensemble
--------------

L’application expose des routes Django « classiques » (HTML).  
Les URLs suivantes sont fournies à titre d’exemple. Adaptez-les à votre projet si besoin.

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
   │   ├── <id>/
   └── profiles/
       ├── <username>/

Formats de réponse
------------------

L’application rend principalement des **templates HTML**.  
Si vous exposez une API JSON (Django REST Framework, par ex.), documentez :

- **méthodes HTTP supportées** (GET/POST/PUT/PATCH/DELETE)
- **schémas de payloads** (entrée/sortie)
- **codes de réponse** (200, 400, 404, 500…)
- **authentification** (session, token, JWT)

Versionnement
-------------

- Prévoir un préfixe de version pour toute API REST publique : ``/api/v1/...``.
- Déprécier proprement (headers, changelog, dates d’EOL).
