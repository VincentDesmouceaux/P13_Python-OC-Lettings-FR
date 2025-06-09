from django.contrib import admin
from django.urls import path, include
from .views import HomeView
from oc_lettings_site.error_views import Error404View, Error500View, CrashTestView


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("lettings/", include("lettings.urls")),
    path("profiles/", include("profiles.urls")),
    path("crash-test-500/", CrashTestView.as_view(), name="crash_test"),
    path("admin/", admin.site.urls),
    path('sentry-debug/', trigger_error),
]

handler404 = Error404View.as_view()
handler500 = Error500View.as_view()
