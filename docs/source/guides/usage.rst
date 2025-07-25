Guide d’utilisation
===================

Cas d’utilisation typiques
--------------------------

1. **Lister les locations**  
   Accédez à :code:`/lettings/`.

2. **Consulter le détail d’une location**  
   Accédez à :code:`/lettings/<id>/`.

3. **Consulter un profil**  
   Accédez à :code:`/profiles/<username>/`.

Gestion des erreurs
-------------------

- Pages **404/500** personnalisées.
- Les erreurs sont **envoyées à Sentry** en production.

FAQ rapide
----------

- **Modifier les textes ?** → dossier :code:`templates/`
- **Changer la base ?** → :doc:`Paramètres & Environnement <../ops/settings>`
- **Ajouter un module ?** → créer une app Django et l’ajouter à ``INSTALLED_APPS``.
