Paramètres & Environnement
==========================

Variables d’environnement (exemples)
------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Nom
     - Description
     - Exemple
   * - ``DJANGO_DEBUG``
     - Active le mode debug Django (dev uniquement)
     - ``True`` / ``False``
   * - ``DJANGO_SECRET_KEY``
     - Clé secrète Django
     - ``changeme``
   * - ``DATABASE_URL``
     - URL de connexion DB (prod)
     - ``postgres://...``
   * - ``SENTRY_DSN``
     - DSN Sentry
     - ``https://...``
   * - ``ALLOWED_HOSTS``
     - Hôtes autorisés (prod)
     - ``myapp.com, ...``

Fichier ``.env``
----------------
...
