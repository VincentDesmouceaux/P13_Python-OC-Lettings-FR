Guide d’utilisation
===================

Cas d’utilisation
-----------------

- **/lettings/** : liste des locations
- **/lettings/<id>/** : détail d’une location
- **/profiles/<username>/** : profil utilisateur

Erreurs
-------

- Pages **404/500** custom
- Erreurs remontées à **Sentry**

FAQ
---

- Textes des templates → ``templates/``
- Paramètres d’environnement → :doc:`ops/settings`
- Ajouter un module → créer une app Django + l’ajouter à ``INSTALLED_APPS``
