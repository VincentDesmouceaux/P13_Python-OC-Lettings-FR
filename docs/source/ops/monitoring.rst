Monitoring & Logs
=================

Objectifs
---------

- **Détecter** les erreurs le plus tôt possible
- **Observer** la performance (latences, erreurs 500)
- **Tracer** les incidents (stacktraces, logs structurés)

Sentry
------

- Configurer ``SENTRY_DSN`` en production
- Attacher la variable ``SENTRY_RELEASE`` (tagging des versions)
- Capturer :
  - erreurs non gérées (500)
  - messages de log ``logging.error``

Logs applicatifs
----------------

- Niveau par défaut : ``INFO`` en prod, ``DEBUG`` en dev
- Standardiser le format (JSON si centralisation)

Métriques
---------

- Nombre de requêtes / seconde
- Temps de réponse médian (p50) et p95
- Taux d’erreurs (4xx / 5xx)

Alerting
--------

- Seuils Sentry (erreurs/minute)
- Alerte de non‑disponibilité (healthcheck down)
- Notifications (Slack, e-mail)

Plan de reprise
---------------

- Sauvegardes DB
- Procédure de rollback
- Rétention des logs
