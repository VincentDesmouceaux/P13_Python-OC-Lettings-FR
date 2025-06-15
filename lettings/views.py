"""Vues des lettings – instrumentation Sentry + logging."""
import logging
from typing import Any

import sentry_sdk
from django.views.generic import ListView, DetailView
from django.http import Http404
from .models import Letting

logger = logging.getLogger(__name__)


class _SentryLoggingMixin:
    """Mixin commun pour taguer la requête et tracer les accès."""

    def dispatch(self, request, *args: Any, **kwargs: Any):
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("view", self.__class__.__name__)
            scope.set_tag("path", request.path)
        logger.info("Page %s consultée", request.path)
        return super().dispatch(request, *args, **kwargs)


class LettingListView(_SentryLoggingMixin, ListView):
    model = Letting
    template_name = "lettings/index.html"
    context_object_name = "lettings_list"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        logger.debug("Nombre de lettings récupérés : %s", self.object_list.count())
        return response


class LettingDetailView(_SentryLoggingMixin, DetailView):
    model = Letting
    template_name = "lettings/letting.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        logger.info("Affichage du détail du letting id=%s", pk)
        try:
            return super().get(request, *args, **kwargs)
        except Letting.DoesNotExist as exc:
            msg = f"Letting introuvable pour id={pk}"
            logger.warning(msg)
            sentry_sdk.capture_exception(exc)
            raise Http404(msg) from exc

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        letting: Letting = self.object  # type: ignore[attr-defined]
        context.update(title=letting.title, address=letting.address)
        logger.debug("Contexte detail letting : %s", context)
        return context
