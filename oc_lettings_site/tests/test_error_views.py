
"""
Tests spécifiques pour les pages d'erreur personnalisées

Ce module contient:
1. Des vues factices pour simuler des scénarios d'erreur
2. Une configuration d'URLs de test
3. Des tests pour vérifier le comportement des pages 404 et 500
"""

from django.http import HttpResponse
from django.test import Client, TestCase, override_settings
from django.urls import include, path

# --------------------------------------------------------------
# 1. Vues factices pour les tests
# --------------------------------------------------------------


def ok_view(_request):
    """
    Vue factice "saine" utilisée pour satisfaire les résolutions d'URL

    Retourne simplement "OK" avec un code 200
    """
    return HttpResponse("OK")


def broken_view(_request):
    """
    Vue factice "cassée" pour déclencher des erreurs 500

    Lève intentionnellement une exception pour simuler une erreur serveur
    """
    raise RuntimeError("Boom")


# --------------------------------------------------------------
# 2. Configuration d'URLs de test
# --------------------------------------------------------------
"""
Configuration minimale d'URLs pour tester les pages d'erreur:

- Crée des routes équivalentes à celles du projet réel
- Permet d'isoler les tests des autres applications
- Évite les erreurs de résolution d'URL (NoReverseMatch)
"""

profiles_patterns = ([path("", ok_view, name="index")], "profiles")
lettings_patterns = ([path("", ok_view, name="index")], "lettings")

urlpatterns = [
    path("", ok_view, name="index"),
    path("boom/", broken_view, name="boom"),
    path("profiles/", include(profiles_patterns)),
    path("lettings/", include(lettings_patterns)),
]

# Client de test configuré pour ne pas lever d'exception
client = Client(raise_request_exception=False)

# --------------------------------------------------------------
# 3. Tests des pages d'erreur
# --------------------------------------------------------------


class TestErrorPages(TestCase):
    """
    Tests fonctionnels pour les pages d'erreur personnalisées

    Vérifie:
    - Le contenu des réponses
    - Les codes HTTP
    - L'affichage des messages personnalisés
    """

    def test_custom_404(self):
        """
        Test de la page 404 personnalisée

        Conditions:
        - Accès à une URL inexistante

        Vérifications:
        1. Code HTTP 404
        2. Présence du message personnalisé dans le contenu
        """
        response = client.get("/does-not-exist/")
        self.assertEqual(response.status_code, 404)
        # Vérifie la présence du texte de la page 404
        self.assertIn(b"Page not found", response.content)

    def test_custom_500(self):
        """
        Test de la page 500 personnalisée

        Conditions:
        - Mode production (DEBUG=False)
        - Vue qui génère intentionnellement une erreur

        Vérifications:
        1. Code HTTP 500
        2. Présence du message personnalisé dans le contenu
        """
        # DEBUG doit être False pour que Django rende la page 500
        with override_settings(ROOT_URLCONF=__name__, DEBUG=False):
            response = client.get("/boom/")
        self.assertEqual(response.status_code, 500)
        # Vérifie la présence du texte de la page 500
        self.assertIn(b"Une erreur interne est survenue.", response.content)
