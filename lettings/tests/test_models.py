"""
Tests unitaires pour les modèles de l'application 'lettings'

Vérifie le comportement des modèles Address et Letting:
1. Pour Address:
   - Teste la représentation textuelle (__str__) du modèle
   - Vérifie que le format retourné correspond à 'NUMÉRO RUE'

2. Pour Letting:
   - Teste la représentation textuelle (__str__) du modèle
   - Vérifie la relation OneToOne avec le modèle Address
   - Confirme que les données associées sont correctement accessibles

Classes de test:
- AddressModelTest: Tests spécifiques au modèle Address
- LettingModelTest: Tests spécifiques au modèle Letting

Méthodes:
- test_str_returns_number_and_street (Address):
    Crée une instance Address et vérifie sa représentation textuelle
    
- test_str_and_address_relation (Letting):
    Crée une instance Letting avec son adresse associée
    Vérifie:
    - La représentation textuelle de la location
    - L'accès aux propriétés de l'adresse associée

Fixtures:
- Pour Address: 42 Baker Street, London, LN, 12345, GBR
- Pour Letting: "Nice flat" avec adresse 1 Main, NYC, NY, 10001, USA

Importance:
- Garantit que les méthodes __str__ retournent les valeurs attendues
- Vérifie l'intégrité des relations entre modèles
- Assure que les données associées sont correctement liées
"""

from django.test import TestCase
from lettings.models import Address, Letting


class AddressModelTest(TestCase):
    """Tests unitaires pour le modèle Address"""

    def test_str_returns_number_and_street(self):
        """Vérifie que la représentation textuelle est 'NUMÉRO RUE'"""
        # Création d'une instance Address
        addr = Address.objects.create(
            number=42,
            street="Baker Street",
            city="London",
            state="LN",
            zip_code=12345,
            country_iso_code="GBR",
        )

        # Vérification de la représentation textuelle
        self.assertEqual(str(addr), "42 Baker Street")


class LettingModelTest(TestCase):
    """Tests unitaires pour le modèle Letting"""

    def test_str_and_address_relation(self):
        """Vérifie la représentation textuelle et la relation avec Address"""
        # Création d'une adresse associée
        addr = Address.objects.create(
            number=1,
            street="Main",
            city="NYC",
            state="NY",
            zip_code=10001,
            country_iso_code="USA"
        )

        # Création d'une location liée à l'adresse
        letting = Letting.objects.create(title="Nice flat", address=addr)

        # Vérifications
        self.assertEqual(str(letting), "Nice flat")  # Représentation textuelle
        self.assertEqual(letting.address.city, "NYC")  # Accès à la ville de l'adresse
