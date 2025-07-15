
"""
oc_lettings_site/tests/test_urls.py
-----------------------------------
Tests unitaires pour la résolution des routes du projet racine.

Ce module vérifie que :
  - la route `/` mappe bien sur HomeView
  - la route `/crash-test-500/` mappe bien sur CrashTestView

Classes :
    MainURLsTest (SimpleTestCase)
        Méthodes de test :
            - test_home_resolves_to_home_view
            - test_crash_resolves_to_crash_view
"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from oc_lettings_site.views import HomeView
from oc_lettings_site.error_views import CrashTestView


class MainURLsTest(SimpleTestCase):
    """Vérifie la résolution des routes du projet racine."""

    def test_home_resolves_to_home_view(self):
        """
        La route nommée 'index' doit résoudre sur HomeView.
        """
        url = reverse("index")
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_crash_resolves_to_crash_view(self):
        """
        La route nommée 'crash_test' doit résoudre sur CrashTestView.
        """
        url = reverse("crash_test")
        self.assertEqual(resolve(url).func.view_class, CrashTestView)
