"""
oc_lettings_site/error_views.py – Pages d’erreur personnalisées + instrumentation logging/Sentry
Ce module définit trois vues pour gérer les erreurs HTTP et vérifier le bon
fonctionnement de la capture d’exceptions par Sentry. :
Classes :
  * Error404View
      • Hérite de TemplateView
      • Intercepte les 404 pour :
          - envoyer un message au niveau WARNING dans Sentry
          - logger un WARN dans les logs
          - renvoyer le template 404.html avec le statut HTTP 404
  * Error500View
      • Hérite de TemplateView
      • Lors d’une erreur serveur (500) :
          - la stack trace est déjà envoyée à Sentry via DjangoIntegration
          - on ajoute un log ERROR pour suivi interne
          - renvoie le template 500.html avec le statut HTTP 500
  * CrashTestView
      • Hérite de View
      • Permet de simuler une RuntimeError pour tester la capture 500:
          - GET /crash-test-500/ lève volontairement une exception
          - Sentry créera un event pour cette erreur
"""

import logging
import sentry_sdk
from django.http import HttpResponse
from django.views.generic import TemplateView, View

# Logger dédié aux vues d’erreur
logger = logging.getLogger(__name__)


class Error404View(TemplateView):
    """
    Vue pour gérer les erreurs 404 "Friendly".
    Comportement :
    --------------
    1) Envoie un message WARNING à Sentry :
       sentry_sdk.capture_message("404 – page not found: {path}", level="warning")
    2) Log un warning dans l’application avec le chemin et le user
    3) Retourne le template '404.html' avec status HTTP 404
    """

    template_name = "404.html"

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        # Capture dans Sentry
        sentry_sdk.capture_message(
            f"404 – page not found: {request.path}",
            level="warning",
        )
        # Logging interne
        logger.warning(
            "404 sur %s (user=%s)",
            request.path,
            request.user.username if request.user.is_authenticated else "Anonymous",
        )
        # Construction de la réponse Django
        response: HttpResponse = super().dispatch(request, *args, **kwargs)
        response.status_code = 404
        return response


class Error500View(TemplateView):
    """
    Vue pour gérer les erreurs serveur 500.
    Comportement :
    --------------
    - Sentry reçoit déjà l’exception grâce à DjangoIntegration
    - On ajoute un log ERROR pour suivi interne
    - Retourne le template '500.html' avec status HTTP 500
    """

    template_name = "500.html"

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        # Logging interne de l’erreur
        logger.error("Affichage page 500 pour %s", request.path)
        response: HttpResponse = super().dispatch(request, *args, **kwargs)
        response.status_code = 500
        return response


class CrashTestView(View):
    """
    Vue pour simuler un crash 500 et tester la capture d’exceptions par Sentry.
    GET requête : lève une RuntimeError pour déclencher un event Sentry.
    """

    def get(self, request, *args, **kwargs) -> HttpResponse:
        raise RuntimeError("Crash test : erreur 500 simulée")
