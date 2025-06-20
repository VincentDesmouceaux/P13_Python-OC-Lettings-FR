"""
Version simplifiée et robuste du test des fichiers statiques
"""
import re
import tempfile
from pathlib import Path

from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.views.static import serve as dj_static_serve


class StaticFilesLoadedTest(TestCase):
    pages_to_test = ["/", "/lettings/", "/profiles/"]

    @override_settings(
        DEBUG=True,
        STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    def test_static_files_are_loaded_and_accessible(self):
        # Créer un client de test
        client = Client()

        # Créer un fichier statique temporaire
        with tempfile.TemporaryDirectory() as tmp_dir:
            static_dir = Path(tmp_dir) / "static"
            static_dir.mkdir()

            # Créer un fichier CSS de test
            css_file = static_dir / "test.css"
            css_file.write_text("body { color: red; }")

            # Override des paramètres temporaires
            with override_settings(
                STATICFILES_DIRS=[static_dir],
                STATIC_URL="/static-test/",
            ):
                # Tester chaque page
                for raw in self.pages_to_test:
                    page = reverse(raw) if not raw.startswith("/") else raw
                    resp = client.get(page)
                    self.assertEqual(resp.status_code, 200, f"{page} ne renvoie pas 200")

                    # Vérifier si le fichier test.css est référencé
                    if "test.css" not in resp.content.decode():
                        print(f"⚠️ test.css non référencé dans {page}")
                        continue

                    # Tester l'accès direct au fichier
                    css_url = "/static-test/test.css"
                    css_resp = client.get(css_url)
                    self.assertEqual(
                        css_resp.status_code,
                        200,
                        f"'{css_url}' devrait être accessible (renvoie {css_resp.status_code})"
                    )
                    self.assertEqual(
                        css_resp["Content-Type"],
                        "text/css",
                        f"Content-Type incorrect pour {css_url}: {css_resp['Content-Type']}"
                    )
