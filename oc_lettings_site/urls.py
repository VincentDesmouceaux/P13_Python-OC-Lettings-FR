"""
oc_lettings_site/urls.py – Définition des routes principales et gestion des erreurs
Ce module configure les URL globales du projet Django "oc_lettings_site":
  • HomeView         : page d’accueil
  • Lettigs et Profiles : inclusion des routes dédiées
  • Admin            : interface d’administration Django
  • CrashTestView    : route de test 500
Gestion des handlers d’erreur :
  - handler404 : Error404View (page not found)
  - handler500 : Error500View (internal server error)
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from .views import HomeView
from oc_lettings_site.error_views import Error404View, Error500View, CrashTestView


def boom(_request):
    return 1 / 0


urlpatterns = [
    # Page d’accueil
    path("", HomeView.as_view(), name="index"),
    # Applications métiers : Lettings et Profiles
    path("lettings/", include("lettings.urls")),
    path("profiles/", include("profiles.urls")),
    # Route pour simuler un crash serveur (500)
    path("crash-test-500/", CrashTestView.as_view(), name="crash_test"),
    # Interface d’administration
    path("admin/", admin.site.urls),
]
# Handlers d’erreur personnalisés
handler404 = Error404View.as_view()
handler500 = Error500View.as_view()

if settings.PROD:
    urlpatterns += [
        path("debug/boom", boom, name="debug_boom"),
    ]
