from django.views.generic import ListView, DetailView
from .models import Profile


class ProfileListView(ListView):
    model = Profile
    template_name = "profiles/index.html"
    context_object_name = "profiles_list"


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profiles/profile.html"
    slug_field = "user__username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):  # noqa: D401
        # lookup by username for readability
        return Profile.objects.select_related("user").get(user__username=self.kwargs["username"])
