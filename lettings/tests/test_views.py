"""
Tests d'intégration pour les vues de l'application 'lettings'
Vérifie le bon fonctionnement des vues principales:
1. La vue de liste (index) des locations
2. La vue de détail d'une location spécifique
Méthodes de test:
- setUp: Crée un environnement de test avec une adresse et une location
- test_index_view_lists_lettings:
    Vérifie que la vue index liste correctement les locations
    Contrôles:
    - La réponse contient le titre de la location créée
    - Le template correct est utilisé
- test_detail_view_displays_address:
    Vérifie que la vue de détail affiche correctement les informations
    Contrôles:
    - La réponse contient le titre de la location
    - La réponse contient la ville de l'adresse associée
    - Le template correct est utilisé
Fixtures:
- Crée une adresse de test: 7 Oak, Austin, TX, 73301, USA
- Crée une location de test: "Lake House" liée à l'adresse
Techniques utilisées:
- Reverse URL lookup pour obtenir les URLs des vues
- Client de test Django pour simuler des requêtes HTTP
- Assertions spécialisées (assertContains, assertTemplateUsed)
"""

from django.test import TestCase
from django.urls import reverse
from lettings.models import Address, Letting


class LettingsViewsTest(TestCase):
    """Suite de tests pour les vues de l'application lettings"""

    def setUp(self):
        """Prépare les données de test communes à tous les cas"""
        # Création d'une adresse de test
        addr = Address.objects.create(
            number=7,
            street="Oak",
            city="Austin",
            state="TX",
            zip_code=73301,
            country_iso_code="USA",
        )
        # Création d'une location associée
        self.letting = Letting.objects.create(title="Lake House", address=addr)

    def test_index_view_lists_lettings(self):
        """Teste l'affichage de la liste des locations"""
        # Accès à la vue index via reverse URL lookup
        response = self.client.get(reverse("lettings:index"))
        # Vérifications
        self.assertContains(response, "Lake House")  # Contenu attendu
        self.assertTemplateUsed(response, "lettings/index.html")  # Template correct

    def test_detail_view_displays_address(self):
        """Teste l'affichage du détail d'une location"""
        # Construction de l'URL avec l'ID de la location
        url = reverse("lettings:detail", kwargs={"pk": self.letting.pk})
        response = self.client.get(url)
        # Vérifications du contenu
        self.assertContains(response, "Lake House")  # Titre de la location
        self.assertContains(response, "Austin")  # Ville de l'adresse
        self.assertTemplateUsed(response, "lettings/letting.html")  # Template correct
