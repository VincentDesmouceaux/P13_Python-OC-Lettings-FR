from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()


class ProfilesViewsTest(TestCase):
    """Index + detail CBVs."""

    def setUp(self):
        self.user = User.objects.create_user("bob", password="pwd")
        self.profile = Profile.objects.create(user=self.user, favorite_city="Berlin")

    def test_index_view_lists_usernames(self):
        response = self.client.get(reverse("profiles:index"))
        self.assertContains(response, "bob")
        self.assertTemplateUsed(response, "profiles/index.html")

    def test_detail_view_shows_favorite_city(self):
        url = reverse("profiles:detail", kwargs={"username": "bob"})
        response = self.client.get(url)
        self.assertContains(response, "Berlin")
        self.assertTemplateUsed(response, "profiles/profile.html")
