Base de données & modèles
=========================

Architecture modulaire
----------------------

Nous avons séparé **l’ancienne base monolithique** en **2 apps dédiées** :

- **lettings** : ``Address``, ``Letting``
- **profiles** : ``Profile``

Le tout orchestré par l’app racine **oc_lettings_site** (settings, urls, etc.).

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
