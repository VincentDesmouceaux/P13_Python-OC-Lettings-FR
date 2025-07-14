"""
profiles/admin.py – Enregistrement du modèle Profile dans l’interface d’administration Django

Ce module configure l’administration Django pour l’application "profiles".
Il s’occupe d’enregistrer le modèle `Profile` afin qu’il soit visible et
modifiable depuis l’admin site.

Fonctionnalité :
    • Register Profile : permet la gestion CRUD des profils via /admin/profiles/profile/
"""
from django.contrib import admin
from .models import Profile

# Enregistre le modèle Profile dans l’interface admin
# afin qu’il soit accessible sous la section "Profiles" avec toutes les
# fonctionnalités standard (liste, création, modification, suppression).
admin.site.register(Profile)
