Orange County Lettings – Doc technique (et un peu plus) 🌴
==========================================================


**Orange County Lettings** est une start-up en pleine expansion sur le marché de la
location de biens immobiliers aux États-Unis. Entre **palmiers, couchers de soleil et belles
maisons**, l’équipe tech accélère — et **vous en faites désormais partie**.

Dominique, notre CTO, vous confie une mission claire :

- **Refondre l’architecture** (modularisation Django),
- **Réduire la dette technique** (lint, tests, pages d’erreur, docstrings),
- **Mettre en place un pipeline CI/CD** complet (Docker, Northflank),
- **Superviser finement l’appli avec Sentry**,
- **Rédiger une documentation technique** claire, accessible, *et vivante* (ce que vous lisez).

Cette documentation vous guide de bout en bout : **démarrage local (en conteneur prod-like),**
**déploiement automatisé**, **surveillance**, et **maintenance** — tout ce dont
aura besoin la prochaine recrue pour être efficace… dès le premier café.

.. toctree::
   :maxdepth: 2
   :caption: Aperçu

   introduction
   quickstart
   tech_stack
   database
   installation_docker
   quickstart_docker
   installation

.. toctree::
   :maxdepth: 2
   :caption: Architecture & Interfaces

   api/index

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/usage

.. toctree::
   :maxdepth: 2
   :caption: Ops

   ops/settings
   ops/ci_cd
   ops/deployment
   ops/monitoring
   ops/makefile
