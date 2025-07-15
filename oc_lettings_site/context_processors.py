"""
oc_lettings_site/context_processors.py – Exposition du DSN Sentry aux templates
Ce module fournit un context processor Django pour rendre disponible
la variable d’environnement `SENTRY_DSN` dans tous les gabarits (templates).
Fonction :
    sentry_dsn(request) -> dict
        - Récupère la valeur de l’URL DSN Sentry depuis les variables d’environnement.
        - Renvoie un dictionnaire avec la clé `SENTRY_DSN`, accessible dans le contexte.
Usage :
    Dans `settings.py`, ajouter le chemin `"oc_lettings_site.context_processors.sentry_dsn"`
    à la liste `TEMPLATES[...]['OPTIONS']['context_processors']`, par exemple :
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # ... autres processors Django ...
                    'oc_lettings_site.context_processors.sentry_dsn',
                ],
            },
        },
    ]
"""

import os
from typing import Any, Dict


def sentry_dsn(_request: Any) -> Dict[str, str]:
    """
    Ajoute `SENTRY_DSN` au contexte global des templates.
    Paramètres :
    -----------
    _request : HttpRequest
        Requête HTTP entrante (non utilisée ici).
    Retour :
    -------
    dict :
        {'SENTRY_DSN': valeur_du_DSN}
        La clé `SENTRY_DSN` peut être référencée dans les templates via `{{ SENTRY_DSN }}`.
    """
    return {"SENTRY_DSN": os.getenv("SENTRY_DSN", "")}
