Monitoring & Logs
=================

Objectifs
---------

- **Voir** les erreurs le plus tôt possible
- **Comprendre** quel déploiement a introduit quoi
- **Tracer** pour réagir et corriger

Sentry
------

- ``SENTRY_DSN`` doit être présent en prod
- **Release = SHA** du build (`SENTRY_RELEASE`)
- Logs + erreurs non gérées (500) automatiquement remontés

Logging applicatif
------------------

- Niveau **INFO** en prod, **DEBUG** local si besoin
- Standardiser le format (JSON si centralisé)

Métriques à surveiller
----------------------

- Temps de réponse (p50/p95)
- Taux d’erreurs (4xx/5xx)
- Disponibilité (healthcheck)

Alerte
------

- Seuils Sentry (ex. erreurs/minute)
- Notifications Slack / e‑mail

Plan de reprise
---------------

- Sauvegardes DB
- Rollback par tag Docker + migrations inverses
