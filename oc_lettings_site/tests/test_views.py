
"""
oc_lettings_site/tests/test_views.py
------------------------------------
Tests d’intégration pour les vues principales de l’application Django.

Ce module vérifie :
  - la page d’accueil (HomeView) renvoie bien le template `index.html`
    et le code HTTP 200.
  - le handler 404 personnalisé (Error404View) renvoie `404.html` et
    HTTP 404 lorsque DEBUG=False.
  - le handler 500 personnalisé (CrashTestView → Error500View) renvoie
    `500.html` et HTTP 500 lorsque DEBUG=False.

Classes :
    MainViewsTest (TestCase)
        Méthodes de test :
            - test_home_ok : page d’accueil
            - test_custom_404_page
            - test_custom_500_page
"""
from django.test import TestCase
from django.urls import reverse


class MainViewsTest(TestCase):
    """Intégration : Home + handlers 404 et 500."""

    def test_home_ok(self):
        """
        La vue d’accueil doit renvoyer HTTP 200 et utiliser `index.html`.
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_custom_404_page(self):
        """
        En DEBUG=False, une URL inexistante doit déclencher Error404View
        et renvoyer `404.html` avec HTTP 404.
        """
        with self.settings(
            ROOT_URLCONF="oc_lettings_site.urls",
            DEBUG=False,
        ):
            response = self.client.get("/page-inexistante/")
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, "404.html")

    def test_custom_500_page(self):
        """
        En DEBUG=False, accéder à `/crash-test-500/` (RuntimeError)
        doit déclencher Error500View et renvoyer `500.html` avec HTTP 500.
        """
        # Empêche pytest de remonter l’exception au client
        self.client.raise_request_exception = False
        with self.settings(
            ROOT_URLCONF="oc_lettings_site.urls",
            DEBUG=False,
        ):
            response = self.client.get(reverse("crash_test"))
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, "500.html")
