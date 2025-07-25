"""
Modèles de données pour l'application 'lettings'
Contient deux modèles principaux :
1. Address - Représente une adresse postale complète
2. Letting - Représente une annonce de location avec une adresse associée
Relations:
- Une Letting est liée à une seule Address via une relation OneToOne
  (Une adresse ne peut être utilisée que par une seule annonce)
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """
    Modèle d'adresse postale
    Champs:
    - number: Numéro dans la rue (1-9999)
    - street: Nom de la rue (max 64 caractères)
    - city: Ville (max 64 caractères)
    - state: État/Province (code à 2 lettres exactement)
    - zip_code: Code postal (5 chiffres)
    - country_iso_code: Code pays ISO (3 lettres exactement)
    Méthodes:
    - __str__: Représentation sous forme 'NUMÉRO RUE' (ex: '123 Main')
    Métadonnées:
    - Noms singulier/pluriel dans l'admin: Address/Addresses
    """

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    def __str__(self) -> str:
        return f"{self.number} {self.street}"

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Letting(models.Model):
    """
    Modèle d'annonce de location immobilière
    Champs:
    - title: Titre de l'annonce (max 256 caractères)
    - address: Relation OneToOne vers le modèle Address
      (Suppression en cascade: si l'adresse est supprimée, l'annonce l'est aussi)
    Méthodes:
    - __str__: Retourne le titre de l'annonce
    """

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
