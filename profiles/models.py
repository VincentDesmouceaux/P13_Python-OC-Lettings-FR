from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extra user data stored outside the built-in User model.
    We keep a temporary related_name to avoid clashing with the
    legacy model until it gets deleted in a later migration.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",      # <-- AJOUT
    )
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self) -> str:  # noqa: D401
        return self.user.username
