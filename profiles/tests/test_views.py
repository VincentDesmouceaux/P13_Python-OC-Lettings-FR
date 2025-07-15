"""
profiles/tests.py – Jeux de tests pour les vues Profiles
Ce module contient les tests automatisés pour les vues CBV `ProfileListView`
et `ProfileDetailView`. Il vérifie que :
  • La page d’index liste bien les noms d’utilisateur.
  • La page de détail affiche la ville favorite et utilise le bon template.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()


class ProfilesViewsTest(TestCase):
    """
    Tests fonctionnels des vues de l’application "profiles".
    Méthodes de test :
    ------------------
    - test_index_view_lists_usernames : vérifie que l’index affiche les usernames
    - test_detail_view_shows_favorite_city : vérifie que le détail affiche la ville favorite
    """

    def setUp(self) -> None:
        """
        Prépare un utilisateur et son profil avant chaque test.
        Attribue :
        - self.user    : instance User avec username 'bob'
        - self.profile : instance Profile associée à self.user
        """
        self.user = User.objects.create_user(username="bob", password="pwd")
        self.profile = Profile.objects.create(user=self.user, favorite_city="Berlin")

    def test_index_view_lists_usernames(self) -> None:
        """
        La vue d’index (/profiles/) doit :
        - renvoyer le template 'profiles/index.html'
        - contenir le username 'bob' dans le contenu HTML
        """
        response = self.client.get(reverse("profiles:index"))
        self.assertContains(
            response,
            self.user.username,
            msg_prefix="Le nom d’utilisateur doit apparaître sur la page d’index",
        )
        self.assertTemplateUsed(response, "profiles/index.html")

    def test_detail_view_shows_favorite_city(self) -> None:
        """
        La vue de détail (/profiles/<username>/) doit :
        - renvoyer le template 'profiles/profile.html'
        - contenir la valeur favorite_city du profil
        """
        url = reverse("profiles:detail", kwargs={"username": self.user.username})
        response = self.client.get(url)
        self.assertContains(
            response,
            self.profile.favorite_city,
            msg_prefix="La ville favorite doit apparaître sur la page de détail",
        )
        self.assertTemplateUsed(response, "profiles/profile.html")
