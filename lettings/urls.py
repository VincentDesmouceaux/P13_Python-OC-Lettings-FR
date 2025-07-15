"""
Configuration des URL pour l'application 'lettings'

Définit les routes pour :
1. La liste des locations (vue d'index)
2. Le détail d'une location spécifique

Patterns d'URL :
- '' (racine) : 
    Vue : LettingListView (liste de toutes les locations)
    Nom : 'index'
    
- '<int:pk>/' (détail par ID) : 
    Vue : LettingDetailView (détails d'une location spécifique)
    Nom : 'detail'

Conventions :
- Utilise des vues basées sur des classes (Class-Based Views)
- L'identifiant 'pk' (Primary Key) est passé comme paramètre numérique
- Namespace d'application : 'lettings' (pour le reverse URL lookup)

Exemples d'utilisation :
{% url 'lettings:index' %}
{% url 'lettings:detail' letting_id=1 %}
"""

from django.urls import path
from .views import LettingListView, LettingDetailView

app_name = "lettings"

urlpatterns = [
    path("", LettingListView.as_view(), name="index"),
    path("<int:pk>/", LettingDetailView.as_view(), name="detail"),
]
