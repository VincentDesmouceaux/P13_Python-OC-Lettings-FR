Base de données & modèles
=========================

Architecture modulaire
----------------------

Nous avons séparé **l’ancienne base monolithique** en **2 apps dédiées** :

- **lettings** : ``Address``, ``Letting``
- **profiles** : ``Profile``

Le tout orchestré par l’app racine **oc_lettings_site** (settings, urls, etc.).

Modèle conceptuel (simplifié)
-----------------------------

.. mermaid::
   :caption: Modèle conceptuel simplifié

   classDiagram
     class Profile {
       +id: int
       +user: OneToOne(User)
       +favorite_city: str
     }

     class Address {
       +id: int
       +number: int
       +street: str
       +city: str
       +state: str
       +zip_code: str
       +country_iso_code: str
     }

     class Letting {
       +id: int
       +title: str
       +address: FK(Address)
     }

     Profile --> "1" User
     Letting --> "1" Address

Migrations – stratégie
----------------------

- **Créer les nouvelles apps** (``lettings``, ``profiles``) + **migrations de données**
- **Supprimer les anciennes tables** via migrations Django (pas de SQL brut)
- **Ne rien casser côté admin / URLs / templates** (refacto pure)
