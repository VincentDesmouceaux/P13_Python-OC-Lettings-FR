"""
Expose par défaut les réglages de base pour
`import oc_lettings_site.settings`.

Le CI (pytest, manage.py…) continue ainsi
d'utiliser le chemin historique.
"""
from .base import *  # noqa: F401,F403
