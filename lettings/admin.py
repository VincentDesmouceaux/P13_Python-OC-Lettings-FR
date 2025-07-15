"""
Configuration de l'interface d'administration pour l'application 'lettings'

Fonctionnalités principales:
1. Enregistrement des modèles Address et Letting avec des classes Admin personnalisées
2. Surveillance des connexions admin via des signaux Django
3. Intégration avec Sentry pour le suivi des connexions administrateur

Composants:
- Logging des connexions admin (local et Sentry)
- Configuration d'affichage pour le modèle Address
- Configuration d'affichage pour le modèle Letting

Signaux:
- Connecte le signal user_logged_in à une fonction de log personnalisée
  pour capturer spécifiquement les connexions à l'interface d'admin

Sécurité:
- Surveille et logge toutes les connexions à l'interface d'administration
- Envoie des alertes à Sentry pour un suivi centralisé

Personnalisation admin:
- AddressAdmin: 
    Affichage: number, street, city, state, zip_code, country_iso_code
    Recherche: par street et city
    
- LettingAdmin:
    Affichage: title et address
    Recherche: par title
"""

import logging

import sentry_sdk
from django.contrib import admin
from django.contrib.auth.signals import user_logged_in

from .models import Address, Letting

logger = logging.getLogger(__name__)


def log_admin_login(sender, request, user, **kwargs):
    """
    Callback pour le signal de connexion utilisateur

    Envoie une alerte à Sentry et logge localement lorsqu'un utilisateur
    se connecte à l'interface d'administration Django.

    Conditions:
    - Ne se déclenche que pour les URLs commençant par '/admin/'

    Paramètres:
    - sender: Classe de l'expéditeur (non utilisé)
    - request: Objet HttpRequest de la connexion
    - user: Instance de l'utilisateur connecté
    - kwargs: Arguments supplémentaires du signal
    """
    if request.path.startswith('/admin/'):
        message = f"Admin user '{user.username}' has logged in"
        # Envoi à Sentry (niveau info par défaut)
        sentry_sdk.capture_message(message)
        # Log local au niveau INFO
        logger.info(message)


# Connexion du signal sans décorateur (plus explicite)
user_logged_in.connect(log_admin_login)


class AddressAdmin(admin.ModelAdmin):
    """
    Configuration admin pour le modèle Address

    Options:
    - list_display: Affiche tous les champs importants en liste
    - search_fields: Active la recherche par nom de rue et ville
    """
    list_display = (
        "number",
        "street",
        "city",
        "state",
        "zip_code",
        "country_iso_code",
    )
    search_fields = ("street", "city")


class LettingAdmin(admin.ModelAdmin):
    """
    Configuration admin pour le modèle Letting

    Options:
    - list_display: Affiche le titre et l'adresse associée
    - search_fields: Active la recherche par titre de location
    """
    list_display = ("title", "address")
    search_fields = ("title",)


# Enregistrement des modèles avec leurs configurations admin
admin.site.register(Address, AddressAdmin)
admin.site.register(Letting, LettingAdmin)
