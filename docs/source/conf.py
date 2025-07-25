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

language = "fr"
templates_path = ["_templates"]
exclude_patterns: list[str] = []

html_theme = "furo"

# Pour que le dark mode applique un vrai thème de coloration différent
pygments_style = "default"
pygments_dark_style = "native"  # ou "monokai", "stata-dark", ...

# On garde les assets (images, etc.)
html_static_path = ["_static"]

# --- Toute la personnalisation passe ici ---
html_theme_options = {
    # Si tu as des logos dédiés :
    # "light_logo": "img/logo-light.svg",
    # "dark_logo": "img/logo-dark.svg",

    # Bouton de retour en haut (icône flottante Furo)
    "top_of_page_button": "edit",  # "edit" ou "none"

    # Variables CSS claires (mode light)
    "light_css_variables": {
        # -------- Marque / couleurs principales --------
        "color-brand-primary": "#ff7a18",
        "color-brand-content": "#ff7a18",

        # -------- Fond & texte --------
        "color-background-primary": "#fffdfa",
        "color-background-secondary": "#ffffff",
        "color-foreground-primary": "#1f1f1f",
        "color-foreground-secondary": "#4a4a4a",
        "color-accent": "#ff7a18",

        # -------- Liens --------
        "color-link": "#ff7a18",
        "color-link--hover": "#e85f00",
        "color-link-underline": "currentColor",

        # -------- Sidebar / Navigation --------
        "color-sidebar-background": "#fff8ef",
        "color-sidebar-foreground": "#1f1f1f",
        "color-sidebar-link-text": "#1f1f1f",
        "color-sidebar-link-text--top-level": "#1f1f1f",
        "color-sidebar-brand-text": "#ff7a18",
        "color-sidebar-search-background": "#fff",
        "color-sidebar-search-border": "#ffe0c2",

        # -------- Titres / bordures / ombres --------
        "color-toc-title": "#ff7a18",
        "color-api-name": "#ff7a18",
        "color-border": "#ffe2cc",
        "color-problematic": "#b00020",

        # -------- Admonitions --------
        "color-admonition-background": "#fff3e0",
        "color-admonition-title-background": "#ffe8cc",
        "color-admonition-title-foreground": "#1f1f1f",

        # -------- Code blocks --------
        "color-code-background": "#fff7ef",
        "color-code-foreground": "#1f1f1f",

        # -------- Tables --------
        "color-table-border": "#ffe2cc",
        "color-table-row-background": "#ffffff",
        "color-table-row-background--hover": "#fff3e0",

        # -------- Polices --------
        "font-stack": (
            "Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "
            "Noto Sans, sans-serif"
        ),
        "font-stack--monospace": (
            "SFMono-Regular, Menlo, Consolas, Liberation Mono, DejaVu Sans Mono, monospace"
        ),

        # -------- “Design tokens” maison pour + de rondeur --------
        "radius-small": "6px",
        "radius-medium": "10px",
        "radius-large": "16px",
        "shadow-sm": "0 1px 3px rgba(0,0,0,.08)",
        "shadow-md": "0 4px 18px rgba(0,0,0,.08)",
    },

    # Variables CSS sombres (mode dark)
    "dark_css_variables": {
        "color-brand-primary": "#ff9d4d",
        "color-brand-content": "#ff9d4d",

        "color-background-primary": "#151515",
        "color-background-secondary": "#1c1c1c",
        "color-foreground-primary": "#f2f2f2",
        "color-foreground-secondary": "#c7c7c7",
        "color-accent": "#ff9d4d",

        "color-link": "#ff9d4d",
        "color-link--hover": "#ff7a18",
        "color-link-underline": "currentColor",

        "color-sidebar-background": "#1a1a1a",
        "color-sidebar-foreground": "#f2f2f2",
        "color-sidebar-link-text": "#f2f2f2",
        "color-sidebar-link-text--top-level": "#ffffff",
        "color-sidebar-brand-text": "#ff9d4d",
        "color-sidebar-search-background": "#111",
        "color-sidebar-search-border": "#33271f",

        "color-toc-title": "#ff9d4d",
        "color-api-name": "#ff9d4d",
        "color-border": "#2a2a2a",
        "color-problematic": "#ff4d4d",

        "color-admonition-background": "#2a1f18",
        "color-admonition-title-background": "#3b261a",
        "color-admonition-title-foreground": "#f2f2f2",

        "color-code-background": "#1e1a17",
        "color-code-foreground": "#f2f2f2",

        "color-table-border": "#2a2a2a",
        "color-table-row-background": "#1c1c1c",
        "color-table-row-background--hover": "#2a1f18",

        "font-stack": (
            "Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "
            "Noto Sans, sans-serif"
        ),
        "font-stack--monospace": (
            "SFMono-Regular, Menlo, Consolas, Liberation Mono, DejaVu Sans Mono, monospace"
        ),

        "radius-small": "6px",
        "radius-medium": "10px",
        "radius-large": "16px",
        "shadow-sm": "0 1px 3px rgba(0,0,0,.25)",
        "shadow-md": "0 4px 18px rgba(0,0,0,.25)",
    },
}

todo_include_todos = True
nitpicky = False
