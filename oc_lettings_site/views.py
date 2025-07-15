"""
oc_lettings_site/views.py – Vue d’accueil (HomeView)
Ce module contient la vue principale du site, affichant la landing page
avec des liens vers les applications ‘profiles’ et ‘lettings’.
Classes :
    HomeView
        • Hérite de TemplateView
        • Charge le template ‘index.html’
"""

import logging
from django.views.generic import TemplateView

# Initialisation du logger pour ce module
tmp_logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """
    Vue de la page d’accueil (landing page).
    Fonction :
        • Afficher le template `index.html` intégrant les liens vers
          les sections Profiles et Lettings.
    Attributs :
    ----------
    template_name : str
        Chemin du template utilisé (‘index.html’).
    """

    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        """
        Log l’accès à la home page.
        - Enregistre un log INFO indiquant l’URL demandée.
        - Appelle TemplateView.dispatch pour continuer le cycle.
        """
        tmp_logger.info("Home page consultée : %s", request.path)
        return super().dispatch(request, *args, **kwargs)
