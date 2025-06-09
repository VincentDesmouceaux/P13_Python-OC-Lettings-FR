from django.test import SimpleTestCase
from django.urls import resolve, reverse
from profiles.views import ProfileListView, ProfileDetailView


class ProfilesURLsTest(SimpleTestCase):
    def test_index_url_resolves(self):
        self.assertEqual(resolve(reverse("profiles:index")).func.view_class,
                         ProfileListView)

    def test_detail_url_resolves(self):
        url = reverse("profiles:detail", kwargs={"username": "john"})
        self.assertEqual(resolve(url).func.view_class, ProfileDetailView)
