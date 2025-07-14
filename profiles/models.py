"""
profiles/models.py – Définition du modèle Profile

Ce module définit la classe `Profile`, qui étend le modèle utilisateur Django
pour y ajouter des données métiers propres à l’application.

Classes :

    Profile
        - user           : relation OneToOne vers django.contrib.auth.models.User
        - favorite_city  : ville favorite de l’utilisateur (facultatif)
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile lié à un utilisateur Django.

    Attributs :
    -----------
    user : OneToOneField[User]
        Association 1-à-1 avec le modèle User. Si l’utilisateur est supprimé,
        le profil l’est aussi (on_delete=models.CASCADE).
    favorite_city : str
        Ville préférée de l’utilisateur. Champ optionnel (blank=True), limité
        à 64 caractères.

    Méthodes :
    ----------
    __str__(self) -> str
        Représentation en chaîne du profil : renvoie le username de l’utilisateur.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="L’utilisateur propriétaire de ce profil"
    )
    favorite_city = models.CharField(
        max_length=64,
        blank=True,
        help_text="Ville favorite (optionnelle)"
    )

    def __str__(self) -> str:  # noqa: D105
        """
        Retourne le nom d’utilisateur associé, pour l’affichage dans l’admin
        et la console.
        """
        return self.user.username
