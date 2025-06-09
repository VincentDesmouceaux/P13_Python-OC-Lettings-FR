from django.test import TestCase
from lettings.models import Address, Letting


class AddressModelTest(TestCase):
    """Vérifie __str__ et les contraintes du modèle Address."""

    def test_str_returns_number_and_street(self):
        addr = Address.objects.create(
            number=42,
            street="Baker Street",
            city="London",
            state="LN",
            zip_code=12345,
            country_iso_code="GBR",
        )
        self.assertEqual(str(addr), "42 Baker Street")


class LettingModelTest(TestCase):
    """Vérifie __str__ et la relation One-To-One."""

    def test_str_and_address_relation(self):
        addr = Address.objects.create(
            number=1, street="Main", city="NYC",
            state="NY", zip_code=10001, country_iso_code="USA"
        )
        letting = Letting.objects.create(title="Nice flat", address=addr)
        self.assertEqual(str(letting), "Nice flat")
        self.assertEqual(letting.address.city, "NYC")
