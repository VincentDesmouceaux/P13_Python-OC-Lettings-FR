"""
profiles/tests_models.py – Tests unitaires du modèle Profile
Ce module contient un jeu de tests pour la méthode __str__ de la classe Profile.
Il vérifie que la représentation en chaîne d’un profil correspond bien au
username de l’utilisateur associé.
Tests inclus :
  * test_str_returns_username :
      - Création d’un utilisateur et de son profil
      - Assertion que str(profile) == username
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()


class ProfileModelTest(TestCase):
    """
    Test de la méthode __str__ du modèle Profile.
    Cette méthode doit renvoyer la propriété `username` de l’utilisateur.
    """

    def test_str_returns_username(self) -> None:
        """
        Vérifie que l’appel de str(profile) retourne bien le username.
        Étapes :
        1. Création d’un User avec username 'alice'.
        2. Création d’un Profile pour cet utilisateur.
        3. Assertion que str(profile) == 'alice'.
        """
        user = User.objects.create_user(username="alice", password="pass")
        profile = Profile.objects.create(user=user, favorite_city="Paris")
        self.assertEqual(
            str(profile),
            user.username,
            msg="La méthode __str__ doit retourner le username de l’utilisateur",
        )
