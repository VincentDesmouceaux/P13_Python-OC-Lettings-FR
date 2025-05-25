from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Landing page linking to Profiles & Lettings."""

    template_name = "index.html"
