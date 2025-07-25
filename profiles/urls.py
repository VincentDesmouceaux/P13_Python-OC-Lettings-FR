"""
profiles/urls.py – Déclaration des URLs pour l’application Profiles
Ce module définit les routes URL exposées par l’application Django
"profiles" et associe chaque pattern à la vue correspondante.
Routes disponibles :
"""  # noqa: D100

from django.urls import path
from .views import ProfileListView, ProfileDetailView

app_name = "profiles"
urlpatterns = [
    # -------------------------------------------------------------------------
    # Liste des profils
    # URL     : /
    # Vue     : ProfileListView (ListView)
    # Template: profiles/index.html
    # -------------------------------------------------------------------------
    path("", ProfileListView.as_view(), name="index"),
    # -------------------------------------------------------------------------
    # Détail d’un profil (par username)
    # URL pattern : /<username>/
    # Vue          : ProfileDetailView (DetailView)
    # Template     : profiles/profile.html
    # -------------------------------------------------------------------------
    path("<str:username>/", ProfileDetailView.as_view(), name="detail"),
]
