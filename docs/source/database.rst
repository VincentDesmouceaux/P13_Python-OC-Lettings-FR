Base de données & modèles
=========================

Architecture modulaire
----------------------

Nous avons séparé l’ancienne app monolithique en **2 apps dédiées** :

- **lettings** : ``Address``, ``Letting``
- **profiles** : ``Profile``

Le tout orchestré par l’app racine **oc_lettings_site** (settings, urls, etc.).

Chronologie des migrations (sans SQL brut)
------------------------------------------

- **Avant** : ``oc_lettings_site/0001_initial`` crée ``Address``, ``Profile``, ``Letting`` (Django 3.0).
- **Nouveau schéma** :
  
  - ``lettings/0001_initial`` : recrée ``Address`` (PK en ``BigAutoField``) et ``Letting`` (``OneToOne`` → ``Address``).
  - ``profiles/0001_initial`` : crée ``Profile`` avec ``user = OneToOne(User, related_name="profile_new")``.
  - ``profiles/0003_*`` : corrige le ``related_name`` → ``"profile"`` (nom final).
- **Migrations de copie** : ``lettings/0002_copy_data.py`` et ``profiles/0002_copy_data.py`` sont **neutralisées**  
  (``RunPython(noop, noop)``, ``elidable=True``) afin de :
  
  * préserver l’historique des migrations,
  * permettre des installations **from scratch** et les tests,
  * éviter tout accès à des modèles supprimés.
- **Nettoyage** : ``oc_lettings_site/0002_*`` supprime les anciens modèles via des **opérations Django**
  (``RemoveField`` puis ``DeleteModel``) — *pas* de ``DROP TABLE`` manuel.

.. note::

   **Install neuve** : seules les tables ``lettings_*`` et ``profiles_*`` existent,
   les migrations “copy” sont sautées (NO-OP), tout fonctionne.

.. warning::

   **Base historique à reprendre** : si des données vivent encore dans ``oc_lettings_site.*``,
   il fallait **exécuter une vraie migration de données** (``RunPython`` via ORM) **avant**
   la suppression. Dans notre dépôt, les migrations de copie sont neutralisées car
   la reprise n’est pas nécessaire dans nos environnements actuels.

Modèles actuels (résumé)
------------------------

- ``lettings.Address`` : ``number/street/city/state/zip_code/country_iso_code``  
  (validators, ``__str__`` → ``"NUMBER STREET"``, ``verbose_name_plural="Addresses"``).
- ``lettings.Letting`` : ``title`` + ``address = OneToOne(Address, on_delete=CASCADE)``.
- ``profiles.Profile`` : ``user = OneToOne(User, related_name="profile")``, ``favorite_city`` (optionnel).

Schéma des tables (PDF)
-----------------------

.. figure:: _static/img/schema_tables.pdf
   :alt: Schéma des tables OC Lettings (PDF)
   :width: 100%
   :align: center

   Structure des tables (ouvrir/zoom selon votre navigateur).

.. only:: html

   .. raw:: html

      <div style="margin:1rem 0;border:1px solid #eee;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.04);">
        <object data="_static/img/schema_tables.pdf" type="application/pdf" width="100%" height="680">
          <p>Votre navigateur ne peut pas afficher le PDF.
             <a href="_static/img/schema_tables.pdf" target="_blank" rel="noopener">Télécharger le schéma</a>.
          </p>
        </object>
      </div>
