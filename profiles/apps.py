"""
profiles/apps.py – Configuration de l’application "profiles"
Ce module définit la classe ProfilesConfig, utilisée par Django pour
configurer l’application "profiles".
Attributs clés :
    default_auto_field : type de champ clé primaire par défaut pour les modèles
    name               : nom Python du module de l’application
"""

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    Classe de configuration pour l’application "profiles".
    - default_auto_field (str) : définit BigAutoField comme type de
      champ clé primaire par défaut pour tous les modèles de cette app.
    - name (str)               : chemin Python vers le package de l'application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "profiles"
