Paramètres & Environnement
==========================

Variables clés
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 45 25

   * - Nom
     - Rôle
     - Exemple
   * - ``DJANGO_DEBUG``
     - Toujours ``False`` en prod
     - ``False``
   * - ``DJANGO_SECRET_KEY``
     - Clé secrète Django
     - ``changeme``
   * - ``DJANGO_ALLOWED_HOSTS``
     - Hôtes autorisés
     - ``*.code.run,localhost``
   * - ``DJANGO_CSRF_TRUSTED_ORIGINS``
     - Origines CSRF
     - ``https://*.code.run``
   * - ``DATABASE_URL``
     - Connexion DB (prod)
     - ``postgres://...``
   * - ``SENTRY_DSN``
     - Monitoring erreurs
     - ``https://...``
   * - ``PORT``
     - Port d’écoute
     - ``8000``
