from django.views.generic import ListView, DetailView
from .models import Letting


class LettingListView(ListView):
    """Display all lettings."""

    model = Letting
    template_name = "lettings/index.html"
    context_object_name = "lettings_list"


class LettingDetailView(DetailView):
    """Detail of a single letting."""

    model = Letting
    template_name = "lettings/letting.html"

    def get_context_data(self, **kwargs):  # noqa: D401
        context = super().get_context_data(**kwargs)
        letting: Letting = self.object  # type: ignore[attr-defined]
        context.update({
            "title": letting.title,
            "address": letting.address,
        })
        return context
