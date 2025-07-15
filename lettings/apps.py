"""
Configuration de l'application Django 'lettings'

Cette classe définit les paramètres de configuration spécifiques à l'application:
- default_auto_field: Définit le type de champ auto-généré par défaut pour les clés primaires
- name: Spécifie le nom complet de l'application (doit correspondre au nom du package)

Héritage:
- Hérite de django.apps.AppConfig pour la configuration standard des applications

Utilisation:
- Cette configuration est référencée dans INSTALLED_APPS via 'lettings.apps.LettingsConfig'
- Permet d'exécuter du code au démarrage de l'application via la méthode ready()
"""

from django.apps import AppConfig


class LettingsConfig(AppConfig):
    # Type de champ auto pour les clés primaires (BigInteger auto-incrémenté)
    default_auto_field = "django.db.models.BigAutoField"

    # Nom complet de l'application (doit correspondre au chemin du module)
    name = "lettings"
