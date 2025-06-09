from django.test import TestCase
from django.urls import reverse
from lettings.models import Address, Letting


class LettingViewsTest(TestCase):
    """Tests ListView et DetailView de l’app lettings."""

    def setUp(self):
        addr = Address.objects.create(
            number=7,
            street="Ocean Drive",
            city="Miami",
            state="FL",
            zip_code=33101,
            country_iso_code="USA",
        )
        self.letting = Letting.objects.create(title="Beach House", address=addr)

    # --- ListView ---
    def test_list_view_status_and_template(self):
        response = self.client.get(reverse("lettings:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lettings/index.html")

    def test_list_view_context_contains_letting(self):
        response = self.client.get(reverse("lettings:index"))
        self.assertIn(self.letting, response.context["lettings_list"])

    # --- DetailView ---
    def test_detail_view_status_and_template(self):
        url = reverse("lettings:detail", args=[self.letting.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lettings/letting.html")

    def test_detail_view_context_values(self):
        url = reverse("lettings:detail", args=[self.letting.pk])
        response = self.client.get(url)
        self.assertEqual(response.context["title"], "Beach House")
        self.assertEqual(response.context["address"], self.letting.address)
