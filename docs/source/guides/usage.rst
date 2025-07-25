Guide d’utilisation
===================

Cas d’utilisation typiques
--------------------------

1. **Lister les locations**  
   Accédez à :code:`/lettings/` pour voir toutes les locations.

2. **Consulter le détail d’une location**  
   Accédez à :code:`/lettings/<id>/` pour afficher les informations complètes.

3. **Consulter un profil**  
   Accédez à :code:`/profiles/<username>/` pour voir la ville préférée d’un utilisateur.

Gestion des erreurs
-------------------

- Pages personnalisées **404/500** (voir :doc:`Monitoring <../ops/monitoring>` pour le suivi).
- Les erreurs sont remontées à **Sentry** en production.

FAQ rapide
----------

- **Où changer les textes des templates ?** → dossier :code:`templates/`.
- **Comment changer la base de données ?** → voir :doc:`Paramètres & Environnement <../ops/settings>`.
- **Comment ajouter un nouveau module ?** → créer une app Django et l’ajouter dans :code:`INSTALLED_APPS`.
