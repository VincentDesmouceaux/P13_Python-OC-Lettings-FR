from django.test import TestCase
from django.urls import reverse
from lettings.models import Address, Letting


class LettingsViewsTest(TestCase):
    """Intégration : list-view et detail-view."""

    def setUp(self):
        addr = Address.objects.create(
            number=7, street="Oak", city="Austin",
            state="TX", zip_code=73301, country_iso_code="USA"
        )
        self.letting = Letting.objects.create(title="Lake House", address=addr)

    def test_index_view_lists_lettings(self):
        response = self.client.get(reverse("lettings:index"))
        self.assertContains(response, "Lake House")
        self.assertTemplateUsed(response, "lettings/index.html")

    def test_detail_view_displays_address(self):
        url = reverse("lettings:detail", kwargs={"pk": self.letting.pk})
        response = self.client.get(url)
        self.assertContains(response, "Lake House")
        self.assertContains(response, "Austin")
        self.assertTemplateUsed(response, "lettings/letting.html")
