"""Vues des profils – instrumentation Sentry + logging."""
from typing import Any
import logging
import sentry_sdk

from django.views.generic import ListView, DetailView
from .models import Profile

logger = logging.getLogger(__name__)


class _SentryLoggingMixin:
    """Ajoute des tags Sentry et trace la consultation dans les logs."""

    def dispatch(self, request, *args: Any, **kwargs: Any):
        user = request.user if request.user.is_authenticated else None

        # — Sentry : enrichit le scope de la requête
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("view", self.__class__.__name__)
            scope.set_tag("path", request.path)
            scope.set_user(
                {
                    "id": getattr(user, "id", None),
                    "username": getattr(user, "username", "Anonymous"),
                }
            )

        # — Logging
        logger.info(
            "Page %s consultée par %s",
            request.path,
            user.username if user else "Anonymous",
        )

        return super().dispatch(request, *args, **kwargs)


class ProfileListView(_SentryLoggingMixin, ListView):
    model = Profile
    template_name = "profiles/index.html"
    context_object_name = "profiles_list"


class ProfileDetailView(_SentryLoggingMixin, DetailView):
    model = Profile
    template_name = "profiles/profile.html"
    slug_field = "user__username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):  # noqa: D401
        return Profile.objects.select_related("user").get(
            user__username=self.kwargs["username"]
        )
