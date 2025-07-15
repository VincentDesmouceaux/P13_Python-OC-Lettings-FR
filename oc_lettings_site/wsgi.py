"""
oc_lettings_site/wsgi.py – Interface WSGI pour déploiement en production
Ce module sert de point d’entrée WSGI pour les serveurs d’application (e.g.,
Gunicorn, uWSGI) afin de lancer l’application Django.
Fonctionnement :
 1. Configure la variable d’environnement `DJANGO_SETTINGS_MODULE` pour
    indiquer à Django où trouver les paramètres du projet.
 2. Expose l’objet WSGI `application` renvoyé par `get_wsgi_application`,
    utilisé par le serveur pour traiter les requêtes HTTP.
Usage :
   Dans Docker ou sur un serveur, la commande de lancement peut être :
       gunicorn oc_lettings_site.wsgi:application -b 0.0.0.0:$PORT
"""

import os
from django.core.wsgi import get_wsgi_application

# Définition du module de settings par défaut si non précisé
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")
# Création de l'application WSGI pour le serveur web
application = get_wsgi_application()
