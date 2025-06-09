# lettings/views.py
import logging

from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse
import sentry_sdk

from .models import Letting

logger = logging.getLogger(__name__)


class LettingListView(ListView):
    """Display all lettings."""
    model = Letting
    template_name = "lettings/index.html"
    context_object_name = "lettings_list"

    def get(self, request, *args, **kwargs):
        logger.info("Accès à la liste des lettings")
        response = super().get(request, *args, **kwargs)
        count = self.get_queryset().count()
        logger.debug("Nombre de lettings récupérés : %d", count)
        return response


class LettingDetailView(DetailView):
    """Detail of a single letting."""
    model = Letting
    template_name = "lettings/letting.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        logger.info("Affichage du détail du letting id=%s", pk)
        try:
            return super().get(request, *args, **kwargs)
        except Letting.DoesNotExist as e:
            msg = f"Letting introuvable pour id={pk}"
            logger.warning(msg)
            sentry_sdk.capture_exception(e)
            raise Http404(msg)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        letting = self.object  # type: ignore[attr-defined]
        context.update({
            "title": letting.title,
            "address": letting.address,
        })
        logger.debug("Contexte du detail view : %r", {
                     "title": letting.title, "address": str(letting.address)})
        return context
