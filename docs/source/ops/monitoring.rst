Monitoring & Logs
=================

Sentry
------

- Activez ``SENTRY_DSN`` pour envoyer les erreurs
- La release est taggée avec ``SENTRY_RELEASE`` (SHA Git)
- Capture :
  - Exceptions non gérées
  - Logs ``logging.error``

Logs
----

- **INFO** en prod
- **DEBUG** jamais activé en prod
- Exploitables dans la console Northflank ou via un agrégateur externe

Alerting
--------

- Seuils Sentry (taux d’erreurs)
- Healthchecks (à ajouter si besoin)
