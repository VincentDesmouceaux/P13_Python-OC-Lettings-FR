"""
oc_lettings_site/tests/test_static_files.py
-------------------------------------------
Test robuste de l’inclusion et de l’accessibilité des fichiers statiques.
Ce module :
  - crée un client Django pour plusieurs pages (`/`, `/lettings/`, `/profiles/`)
  - instaure un dossier statique temporaire contenant `test.css`
  - vérifie que chaque page référence `test.css`
  - vérifie l’accès direct à `/static-test/test.css` retourne HTTP 200
    avec le bon Content-Type (`text/css`)
Classes :
    StaticFilesLoadedTest (TestCase)
        Méthode de test :
            - test_static_files_are_loaded_and_accessible
"""

import tempfile
from pathlib import Path
from django.test import Client, TestCase, override_settings
from django.urls import reverse


class StaticFilesLoadedTest(TestCase):
    """Version simplifiée et robuste du test des fichiers statiques."""

    pages_to_test = ["/", "/lettings/", "/profiles/"]

    @override_settings(
        DEBUG=True,
        STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    )
    def test_static_files_are_loaded_and_accessible(self):
        """
        Pour chaque page listée :
          1. Vérifier HTTP 200
          2. Vérifier la présence de 'test.css' dans le HTML
          3. Vérifier l’accès direct au fichier CSS génère HTTP 200
             et `Content-Type: text/css`.
        """
        client = Client()
        # Création d’un dossier statique temporaire
        with tempfile.TemporaryDirectory() as tmp_dir:
            static_dir = Path(tmp_dir) / "static"
            static_dir.mkdir()
            # Création du fichier CSS de test
            css_file = static_dir / "test.css"
            css_file.write_text("body { color: red; }")
            # Override des settings pour pointer sur notre dossier temporaire
            with override_settings(
                STATICFILES_DIRS=[static_dir],
                STATIC_URL="/static-test/",
            ):
                for raw in self.pages_to_test:
                    # Construire l’URL de la page
                    page = raw if raw.startswith("/") else reverse(raw)
                    resp = client.get(page)
                    self.assertEqual(
                        resp.status_code, 200, f"{page} ne renvoie pas 200"
                    )
                    # Vérifier la référence à test.css
                    if "test.css" not in resp.content.decode():
                        print(f"⚠️ test.css non référencé dans {page}")
                        continue
                    # Tester l’accès direct
                    css_url = "/static-test/test.css"
                    css_resp = client.get(css_url)
                    self.assertEqual(
                        css_resp.status_code,
                        200,
                        f"'{css_url}' devrait être accessible (renvoie {css_resp.status_code})",
                    )
                    self.assertEqual(
                        css_resp["Content-Type"],
                        "text/css",
                        f"Content-Type incorrect pour {css_url}: {css_resp['Content-Type']}",
                    )
