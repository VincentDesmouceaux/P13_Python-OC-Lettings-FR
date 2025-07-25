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
     - Doit rester ``false`` (prod)
     - ``false``
   * - ``DJANGO_SECRET_KEY``
     - Clé secrète Django
     - ``changeme``
   * - ``DJANGO_ALLOWED_HOSTS``
     - Hôtes autorisés
     - ``myapp.com, *.code.run``
   * - ``DJANGO_CSRF_TRUSTED_ORIGINS``
     - Origines CSRF autorisées
     - ``https://*.code.run``
   * - ``SENTRY_DSN``
     - DSN Sentry
     - ``https://...``
   * - ``PORT``
     - Port d’écoute Gunicorn
     - ``8000``

Fichier ``.env``
----------------

- Versionner **un `.env.example`** (jamais le `.env` réel).
- Charger via **variables d’environnement** dans Docker/Northflank.
