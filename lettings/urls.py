# lettings/urls.py
from django.urls import path

from .views import LettingListView, LettingDetailView

app_name = "lettings"

urlpatterns = [
    path("", LettingListView.as_view(), name="index"),
    path("<int:pk>/", LettingDetailView.as_view(), name="detail"),
]
