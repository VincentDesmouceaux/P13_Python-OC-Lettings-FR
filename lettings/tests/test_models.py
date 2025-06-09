from django.test import TestCase
from lettings.models import Address, Letting


class AddressModelTest(TestCase):
    """Test du modèle Address (str & métadonnées)."""

    def setUp(self):
        self.addr = Address.objects.create(
            number=221,
            street="B Baker Street",
            city="London",
            state="LN",
            zip_code=12345,
            country_iso_code="GBR",
        )

    def test_str_representation(self):
        self.assertEqual(str(self.addr), "221 B Baker Street")

    def test_verbose_names(self):
        self.assertEqual(Address._meta.verbose_name, "Address")
        self.assertEqual(Address._meta.verbose_name_plural, "Addresses")


class LettingModelTest(TestCase):
    """Test du modèle Letting et de sa relation OneToOne."""

    def setUp(self):
        addr = Address.objects.create(
            number=1,
            street="Main",
            city="X",
            state="XY",
            zip_code=99999,
            country_iso_code="USA",
        )
        self.letting = Letting.objects.create(title="Villa Serenity", address=addr)

    def test_str_representation(self):
        self.assertEqual(str(self.letting), "Villa Serenity")

    def test_address_relation(self):
        self.assertEqual(self.letting.address.city, "X")
