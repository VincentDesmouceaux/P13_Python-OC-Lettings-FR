"""
oc_lettings_site/apps.py – Configuration de l’application principale
Ce module définit la configuration de l’application Django "oc_lettings_site".
Lors du démarrage, il enregistre la date de dernière modification d’un template
pour garantir que l’image Docker contient bien les versions les plus récentes
Classes :
    OCLettingsSiteConfig(AppConfig)
        - name : nom Python de l’application
Méthodes :
    ready()
        - Chargée après l’initialisation de Django
        - Vérifie l’accessibilité du template 'lettings/index.html'
        - Logge la date de modification du fichier template ou un warning si introuvable
"""

import logging
import os
from django.apps import AppConfig
from django.template.loader import get_template

# Initialisation du logger pour l’application principale
logger = logging.getLogger(__name__)


class OCLettingsSiteConfig(AppConfig):
    """
    Configuration de l’application Django "oc_lettings_site".
    Attributs :
    ----------
    name : str
        Nom Python du package de l’application.
    """

    name = "oc_lettings_site"

    def ready(self) -> None:
        """
        Appelé une fois Django démarré et prêt.
        Fonction :
        ---------
        1. Définit un template de référence pour validation :
           'lettings/index.html'
        2. Tente de charger le template et récupère sa date de modification
        3. Logge un message INFO avec la modification ou WARNING si échec
        """
        template_name = "lettings/index.html"
        try:
            tpl = get_template(template_name)
            mtime = os.path.getmtime(tpl.origin.name)
            logger.info("Template %s chargé (mtime=%s)", template_name, mtime)
        except Exception as exc:  # pragma: no cover
            logger.warning("Template %s introuvable : %s", template_name, exc)
