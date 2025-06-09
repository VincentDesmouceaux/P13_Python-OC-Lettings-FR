from django.test import SimpleTestCase
from django.urls import resolve, reverse
from lettings.views import LettingListView, LettingDetailView


class LettingURLsTest(SimpleTestCase):
    """Vérifie la correspondance des routes vers les vues génériques."""

    def test_index_url_resolves_to_list_view(self):
        url = reverse("lettings:index")
        self.assertEqual(resolve(url).func.view_class, LettingListView)

    def test_detail_url_resolves_to_detail_view(self):
        url = reverse("lettings:detail", args=[1])
        self.assertEqual(resolve(url).func.view_class, LettingDetailView)
