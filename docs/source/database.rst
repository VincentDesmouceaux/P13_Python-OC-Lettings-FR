Base de données (simplifiée)
============================

Diagramme
---------

.. mermaid::
   :caption: Modèle conceptuel

   classDiagram
     class Profile {
       id
       user (OneToOne User)
       favorite_city
     }

     class Address {
       id
       number
       street
       city
       state
       zip_code
       country_iso_code
     }

     class Letting {
       id
       title
       address (FK)
     }

     Profile --> "1" User
     Letting --> "1" Address

Tables clés
-----------

- **profiles_profile** : ``user_id`` (OneToOne → auth_user), ``favorite_city``
- **lettings_address** : adresse complète
- **lettings_letting** : ``title``, ``address_id`` (FK)
