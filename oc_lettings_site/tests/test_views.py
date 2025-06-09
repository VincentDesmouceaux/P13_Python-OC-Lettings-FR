# oc_lettings_site/tests/test_views.py
from django.test import TestCase
from django.urls import reverse


class MainViewsTest(TestCase):
    """Intégration : Home + handlers 404 et 500."""

    def test_home_ok(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_custom_404_page(self):
        # Force l’URLconf du projet + DEBUG=False
        with self.settings(
            ROOT_URLCONF="oc_lettings_site.urls",
            DEBUG=False,
        ):
            response = self.client.get("/page-inexistante/")
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, "404.html")

    def test_custom_500_page(self):
        # Évite que le client remonte l’exception
        self.client.raise_request_exception = False
        with self.settings(
            ROOT_URLCONF="oc_lettings_site.urls",
            DEBUG=False,
        ):
            response = self.client.get(reverse("crash_test"))
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, "500.html")
