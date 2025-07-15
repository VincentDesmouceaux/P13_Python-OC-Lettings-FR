"""
oc_lettings_site/asgi.py – Interface ASGI pour le déploiement asynchrone
Ce module sert de point d’entrée ASGI pour les serveurs supportant
ASGI (e.g., Daphne, Uvicorn), permettant de lancer l’application Django
en mode asynchrone.
Fonctionnement :
 1. Définit la variable d’environnement DJANGO_SETTINGS_MODULE
    pour indiquer à Django où trouver la configuration du projet.
 2. Charge et expose l’objet ASGI `application` via `get_asgi_application()`,
    utilisé par le serveur ASGI pour traiter les requêtes HTTP/ASGI.
Usage :
   Dans un environnement ASGI, lancer le serveur avec une commande du type :
       uvicorn oc_lettings_site.asgi:application --host 0.0.0.0 --port $PORT
Variables d’environnement attendues :
  • DJANGO_SETTINGS_MODULE : chemin vers le module de settings Django
"""

import os
from django.core.asgi import get_asgi_application

# Configuration du module de settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")
# Création de l’application ASGI
application = get_asgi_application()
