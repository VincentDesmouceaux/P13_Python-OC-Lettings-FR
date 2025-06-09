# profiles/migrations/0002_copy_data.py
from django.db import migrations


def noop(apps, schema_editor):
    """Migration neutralisée : plus de données à copier depuis l’app legacy."""
    return


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
    ]
    elidable = True
    operations = [migrations.RunPython(noop, noop)]
