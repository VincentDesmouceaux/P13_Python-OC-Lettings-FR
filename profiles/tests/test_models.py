from django.test import TestCase
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()


class ProfileModelTest(TestCase):
    """Test simple de __str__."""

    def test_str_returns_username(self):
        user = User.objects.create_user(username="alice", password="pass")
        profile = Profile.objects.create(user=user, favorite_city="Paris")
        self.assertEqual(str(profile), "alice")
