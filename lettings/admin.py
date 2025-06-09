# lettings/admin.py
import logging

import sentry_sdk
from django.contrib import admin
from django.contrib.auth.signals import user_logged_in

from .models import Address, Letting

logger = logging.getLogger(__name__)


def log_admin_login(sender, request, user, **kwargs):
    """
    Envoie un message à Sentry et logge localement lorsqu'un utilisateur
    se connecte à l'admin.
    """
    if request.path.startswith('/admin/'):
        message = f"Admin user '{user.username}' has logged in"
        # Envoi à Sentry
        sentry_sdk.capture_message(message)
        # Log local
        logger.info(message)


# Connexion du signal sans décorateur
user_logged_in.connect(log_admin_login)


class AddressAdmin(admin.ModelAdmin):
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
    list_display = ("title", "address")
    search_fields = ("title",)


# Enregistrement des modèles
admin.site.register(Address, AddressAdmin)
admin.site.register(Letting, LettingAdmin)
