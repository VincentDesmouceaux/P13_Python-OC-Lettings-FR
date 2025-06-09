from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """Landing page linking to Profiles & Lettings."""

    template_name = "index.html"
