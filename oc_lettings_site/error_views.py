
from django.views.generic import TemplateView, View
from django.http import HttpResponse


class Error404View(TemplateView):
    """Custom 404 page."""
    template_name = "404.html"

    def get(self, request, *args, **kwargs):
        # rend le template puis force le code 404
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response


class Error500View(TemplateView):
    """Custom 500 page."""
    template_name = "500.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 500
        return response


class CrashTestView(View):
    """Déclenche volontairement une exception pour tester le handler 500."""

    def get(self, request, *args, **kwargs) -> HttpResponse:
        raise RuntimeError("Crash test : erreur 500 simulée")
