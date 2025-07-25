# docs/source/conf.py
from __future__ import annotations
from datetime import datetime

project = "Orange County Lettings – Documentation"
author = "Équipe Tech OC Lettings"
current_year = datetime.now().year
copyright = f"{current_year}, {author}"
release = "dev"

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinxcontrib.mermaid",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", "https://docs.python.org/3/objects.inv"),
    "django": ("https://docs.djangoproject.com/en/4.2/", "https://docs.djangoproject.com/en/4.2/objects.inv"),
}

todo_include_todos = True

language = "fr"
templates_path = ["_templates"]
exclude_patterns: list[str] = []

html_theme = "furo"
html_static_path = ["_static"]

# >>> CSS custom "sunset & palm trees" :)
html_css_files = [
    "css/oc.css",
]

# Furo: quelques options (facultatif)
html_theme_options = {
    "light_logo": "images/logo-oclettings-light.png",
    "dark_logo": "images/logo-oclettings-dark.png",
}
