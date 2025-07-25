Base de données & modèles
=========================

Structure conceptuelle
----------------------

.. mermaid::
   :caption: Modèle conceptuel simplifié

   classDiagram
     class Profile {
       +id: int
       +user: OneToOne(User)
       +favorite_city: str
       __str__()
     }

     class Address {
       +id: int
       +number: int
       +street: str
       +city: str
       +state: str
       +zip_code: str
       +country_iso_code: str
       __str__()
     }

     class Letting {
       +id: int
       +title: str
       +address: FK(Address)
       __str__()
     }

     Profile --> "1" User
     Letting --> "1" Address

Tables principales
------------------

**profiles_profile**

- ``id`` (PK)
- ``user_id`` (OneToOne → ``auth_user``)
- ``favorite_city``

**lettings_address**

- ``id`` (PK)
- ``number``, ``street``, ``city``, ``state``, ``zip_code``, ``country_iso_code``

**lettings_letting**

- ``id`` (PK)
- ``title``
- ``address_id`` (FK → ``lettings_address``)

Migrations
----------

- Versionnées via Django (``python manage.py makemigrations`` / ``migrate``).
- Stratégie : **small & frequent** pour faciliter les rollbacks.
