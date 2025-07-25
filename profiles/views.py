"""profiles/views.py -- Vues des profils avec instrumentation Sentry et logging."""

from typing import Any
import logging
import sentry_sdk
from django.views.generic import ListView, DetailView
from .models import Profile

# Initialisation du logger pour ce module
tmp_logger = logging.getLogger(__name__)


class _SentryLoggingMixin:
    """
    Mixin pour enrichir chaque vue de profils avec :
    1. Des tags Sentry pour suivre l'exécution côté backend.
    2. Un log d'information indiquant la consultation de la page.
    Fonctions :
      - dispatch : appelé en amont de get/post pour enrichir le scope Sentry
                   et émettre un log côté application.
    """

    def dispatch(self, request, *args: Any, **kwargs: Any):  # noqa: D401
        """
        Override de la méthode `dispatch` pour :
        - Configurer le scope Sentry avec des tags et l'utilisateur.
        - Loguer la consultation de la page.
        Params:
        --------
        request : HttpRequest
            Requête HTTP entrante.
        *args, **kwargs : Any
            Arguments supplémentaires passés par Django.
        Returns:
        --------
        HttpResponse
            Résultat de la méthode dispatch de la super-classe.
        """
        user = request.user if request.user.is_authenticated else None
        # Enrichissement du context Sentry
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("view", self.__class__.__name__)
            scope.set_tag("path", request.path)
            scope.set_user(
                {
                    "id": getattr(user, "id", None),
                    "username": getattr(user, "username", "Anonymous"),
                }
            )
        # Logging de l'accès
        tmp_logger.info(
            "Page %s consultée par %s",
            request.path,
            user.username if user else "Anonymous",
        )
        # Appel à la super-classe pour continuer le cycle de vie\
        return super().dispatch(request, *args, **kwargs)


class ProfileListView(_SentryLoggingMixin, ListView):
    """
    Affiche la liste des profils.
    Hérite de :
      - _SentryLoggingMixin : instrumentation Sentry + logging.
      - ListView de Django : gestion du contexte et rendu template.
    Attributs :
    -----------
    model : django.db.models.Model
        Modèle Django associé (Profile).
    template_name : str
        Chemin du template à rendre.
    context_object_name : str
        Nom de la variable de contexte dans le template.
    """

    model = Profile
    template_name = "profiles/index.html"
    context_object_name = "profiles_list"


class ProfileDetailView(_SentryLoggingMixin, DetailView):
    """
    Affiche le détail d'un seul profil identifié par le username.
    Hérite de :
      - _SentryLoggingMixin : instrumentation Sentry + logging.
      - DetailView de Django : récupération et rendu d'un objet unique.
    Attributs :
    -----------
    model : django.db.models.Model
        Modèle Django associé (Profile).
    template_name : str
        Chemin du template à rendre.
    slug_field : str
        Champ de recherche sur le modèle par slug.
    slug_url_kwarg : str
        Nom du paramètre URL contenant le slug.
    Méthodes :
    ---------
    get_object(queryset=None) -> Profile
        Récupère un Profile en filtrant par user__username pour optimiser
        la requête (select_related).
    """

    model = Profile
    template_name = "profiles/profile.html"
    slug_field = "user__username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None) -> Profile:  # noqa: D401
        """
        Récupère le profil correspondant au username fourni en URL.
        Utilise `select_related` pour pré-charger la relation `user`
        et éviter les requêtes supplémentaires.
        Params:
        -------
        queryset : QuerySet, optional
            QuerySet initial (non utilisé ici).
        Returns:
        --------
        Profile
            Objet Profile associé au username.
        Lève `Profile.DoesNotExist` si aucun profil ne correspond.
        """
        return Profile.objects.select_related("user").get(user__username=self.kwargs["username"])
