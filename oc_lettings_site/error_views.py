"""
oc_lettings_site/error_views.py
-------------------------------
Pages d’erreur personnalisées + instrumentation logging / Sentry
"""

from __future__ import annotations

import logging

import sentry_sdk
from django.http import HttpResponse
from django.views.generic import TemplateView, View

logger = logging.getLogger(__name__)


class Error404View(TemplateView):
    """
    Page 404 « friendly ».

    * Crée un **breadcrumb + event** dans Sentry (niveau WARNING)
    * Trace l’accès dans les logs applicatifs
    * Renvoie votre template 404 avec le bon status HTTP
    """

    template_name = "404.html"

    def dispatch(self, request, *args, **kwargs):  # noqa: D401
        sentry_sdk.capture_message(
            f"404 – page not found: {request.path}",
            level="warning",
        )
        logger.warning(
            "404 sur %s (user=%s)",
            request.path,
            request.user.username if request.user.is_authenticated else "Anonymous",
        )

        response: HttpResponse = super().dispatch(request, *args, **kwargs)
        response.status_code = 404
        return response


class Error500View(TemplateView):
    """
    Page 500.

    L’exception d’origine est déjà envoyée à Sentry par DjangoIntegration.
    On ajoute simplement un log applicatif pour nos dashboard internes.
    """

    template_name = "500.html"

    def dispatch(self, request, *args, **kwargs):  # noqa: D401
        logger.error("Affichage page 500 pour %s", request.path)
        response: HttpResponse = super().dispatch(request, *args, **kwargs)
        response.status_code = 500
        return response


class CrashTestView(View):
    """
    Vue volontairement cassée pour vérifier la capture 500.

    → GET /crash-test-500/ soulève une RuntimeError,
      Sentry doit créer un event « Crash test ».
    """

    def get(self, request, *args, **kwargs) -> HttpResponse:  # noqa: D401
        raise RuntimeError("Crash test : erreur 500 simulée")
