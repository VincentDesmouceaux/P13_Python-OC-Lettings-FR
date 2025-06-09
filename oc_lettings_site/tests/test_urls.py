from django.test import SimpleTestCase
from django.urls import reverse, resolve
from oc_lettings_site.views import HomeView
from oc_lettings_site.error_views import CrashTestView


class MainURLsTest(SimpleTestCase):
    """Vérifie la résolution des routes du projet racine."""

    def test_home_resolves_to_home_view(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_crash_resolves_to_crash_view(self):
        url = reverse("crash_test")
        self.assertEqual(resolve(url).func.view_class, CrashTestView)
