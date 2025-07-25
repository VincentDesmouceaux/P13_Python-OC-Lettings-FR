from __future__ import annotations

from datetime import datetime
from pathlib import Path

project = "P13 Python OC Lettings"
author = "Vincent Desmouceaux"
current_year = datetime.now().year
copyright = f"{current_year}, {author}"
release = "dev"

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinxcontrib.mermaid",
]

intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3",
        "https://docs.python.org/3/objects.inv",
    ),
    "django": (
        "https://docs.djangoproject.com/en/4.2/",
        "https://docs.djangoproject.com/en/4.2/objects.inv",
    ),
}

todo_include_todos = True
language = "fr"

templates_path = ["_templates"]
exclude_patterns: list[str] = []

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]  # <<—— ajoute notre palette « chaleureuse »

nitpicky = False

# Create _static/custom.css if it doesn't exist (safe no-op on RTD)
_static = Path(__file__).parent / "_static"
_static.mkdir(exist_ok=True)
(_static / "custom.css").touch(exist_ok=True)
