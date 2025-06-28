# oc_lettings_site/tests/test_error_views.py
from django.http import HttpResponse
from django.test import Client, TestCase, override_settings
from django.urls import include, path


# ────────────────────────── 1. Vues factices ──────────────────────────
def ok_view(_request):
    """Vue “saine” simplement utilisée pour satisfaire les {% url … %}."""
    return HttpResponse("OK")


def broken_view(_request):
    """Vue volontairement cassée pour déclencher un 500."""
    raise RuntimeError("Boom")


# ───────────────────────── 2. URLconf de test ─────────────────────────
# Les gabarits 404/500 pointent vers index, profiles:index, lettings:index…
# On recrée donc ces routes minimalistes pour éviter les NoReverseMatch.
profiles_patterns = ([path("", ok_view, name="index")], "profiles")
lettings_patterns = ([path("", ok_view, name="index")], "lettings")

urlpatterns = [
    path("", ok_view, name="index"),
    path("boom/", broken_view, name="boom"),
    path("profiles/", include(profiles_patterns)),
    path("lettings/", include(lettings_patterns)),
]

# Un client de test qui **nève** pas l’exception Python quand la vue plante
client = Client(raise_request_exception=False)


# ───────────────────────────── 3. Tests ───────────────────────────────
class TestErrorPages(TestCase):
    """Vérifie que les templates 404 et 500 personnalisés sont servis."""

    def test_custom_404(self):
        response = client.get("/does-not-exist/")
        self.assertEqual(response.status_code, 404)
        # Ajuste au besoin si ton template 404 contient une autre chaîne
        self.assertIn(b"Page not found", response.content)

    def test_custom_500(self):
        # DEBUG doit être False pour que Django rende la page 500
        with override_settings(ROOT_URLCONF=__name__, DEBUG=False):
            response = client.get("/boom/")
        self.assertEqual(response.status_code, 500)
        # Chaîne présente dans templates/500.html
        self.assertIn(b"Une erreur interne est survenue.", response.content)
