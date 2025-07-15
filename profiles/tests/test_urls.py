"""
profiles/tests_urls.py – Tests unitaires des résolutions d’URLs pour Profiles
Ce module vérifie que les noms de routes (namespace + name) définis
pour l’application `profiles` correspondent bien aux classes de vues
attendues. Il utilise `SimpleTestCase` pour résoudre et comparer
les URLs sans nécessiter de base de données.
Tests inclus :
  • test_index_url_resolves : la route `profiles:index` renvoie à ProfileListView
  • test_detail_url_resolves: la route `profiles:detail` renvoie à ProfileDetailView
"""

from django.test import SimpleTestCase
from django.urls import resolve, reverse
from profiles.views import ProfileListView, ProfileDetailView


class ProfilesURLsTest(SimpleTestCase):
    """
    Vérifie la résolution des URLs vers les vues correspondantes.
    Méthodes :
    ---------
    test_index_url_resolves :
        - construit l’URL via `reverse('profiles:index')`
        - s’assure que la vue associée est bien `ProfileListView`
    test_detail_url_resolves :
        - construit l’URL via `reverse('profiles:detail', kwargs={'username': 'john'})`
        - s’assure que la vue associée est `ProfileDetailView`
    """

    def test_index_url_resolves(self) -> None:
        """
        La route `/profiles/` doit pointer vers `ProfileListView`.
        """
        path = reverse("profiles:index")
        resolved = resolve(path)
        self.assertEqual(
            resolved.func.view_class,
            ProfileListView,
            msg="La route 'profiles:index' ne pointe pas vers ProfileListView",
        )

    def test_detail_url_resolves(self) -> None:
        """
        La route `/profiles/<username>/` doit pointer vers `ProfileDetailView`.
        """
        path = reverse("profiles:detail", kwargs={"username": "john"})
        resolved = resolve(path)
        self.assertEqual(
            resolved.func.view_class,
            ProfileDetailView,
            msg="La route 'profiles:detail' ne pointe pas vers ProfileDetailView",
        )
