from django.contrib import admin
from django.urls import path, include
from .views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("lettings/", include("lettings.urls")),
    path("profiles/", include("profiles.urls")),
    path("admin/", admin.site.urls),
]
