# docs/source/conf.py

from __future__ import annotations
from datetime import datetime

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
html_css_files = ["css/oc.css"]  # si tu l'utilises

nitpicky = False
