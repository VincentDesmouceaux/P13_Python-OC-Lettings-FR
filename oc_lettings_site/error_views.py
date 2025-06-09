from django.views.generic import TemplateView
from django.http import HttpResponseServerError, HttpResponseNotFound, HttpResponse
from django.views import View


class Error404View(TemplateView):
    """Custom 404 page (class-based)."""
    template_name = "404.html"

    # handler404 doit renvoyer HttpResponseNotFound
    def __call__(self, request, exception=None):
        response = super().__call__(request, exception=exception)
        return HttpResponseNotFound(response.rendered_content)


class Error500View(TemplateView):
    """Custom 500 page (class-based)."""
    template_name = "500.html"

    # handler500 n’a pas d’exception ; on renvoie 500
    def __call__(self, request):
        response = super().__call__(request)
        return HttpResponseServerError(response.rendered_content)


class CrashTestView(View):
    """Vue volontairement cassée pour déclencher le handler 500 en local."""

    def get(self, request, *args, **kwargs) -> HttpResponse:  # noqa: D401
        # On lève une erreur pour tester la page 500
        raise RuntimeError("Crash test : erreur 500 simulée")
