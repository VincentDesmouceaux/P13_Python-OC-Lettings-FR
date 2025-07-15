"""
Tests unitaires pour les configurations d'URL de l'application 'lettings'

Vérifie que les routes d'URL sont correctement mappées aux vues appropriées:
1. Teste que l'URL d'index ('') est liée à la vue LettingListView
2. Teste que l'URL de détail ('<int:pk>/') est liée à la vue LettingDetailView

Méthodes de test:
- test_index_url_resolves_to_list_view:
    Utilise reverse() pour obtenir l'URL nommée 'index'
    Vérifie avec resolve() que la vue associée est LettingListView
    
- test_detail_url_resolves_to_detail_view:
    Utilise reverse() pour obtenir l'URL nommée 'detail' avec un argument pk=1
    Vérifie avec resolve() que la vue associée est LettingDetailView

Techniques utilisées:
- reverse(): Génération d'URL à partir des noms de vue
- resolve(): Analyse d'URL pour obtenir la fonction/vue correspondante
- SimpleTestCase: Classe de test optimisée pour les tests sans base de données

Importance:
- Garantit que la configuration des URLs reste cohérente avec les vues
- Protège contre les erreurs de refactorisation des noms de vues ou d'URLs
"""

from django.test import SimpleTestCase
from django.urls import resolve, reverse
from lettings.views import LettingListView, LettingDetailView


class LettingURLsTest(SimpleTestCase):
    """Suite de tests pour les configurations d'URL de l'application lettings"""

    def test_index_url_resolves_to_list_view(self):
        """Vérifie que l'URL d'index est mappée sur LettingListView"""
        # Génère l'URL absolue pour la vue 'index'
        url = reverse("lettings:index")

        # Résout l'URL et vérifie la classe de vue associée
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, LettingListView)

    def test_detail_url_resolves_to_detail_view(self):
        """Vérifie que l'URL de détail est mappée sur LettingDetailView"""
        # Génère l'URL pour la vue 'detail' avec pk=1
        url = reverse("lettings:detail", args=[1])

        # Résout l'URL et vérifie la classe de vue associée
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, LettingDetailView)
