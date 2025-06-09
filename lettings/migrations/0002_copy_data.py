# lettings/migrations/0002_copy_data.py
"""Migration d’origine (copie de données legacy) neutralisée.

   Les anciens modèles `oc_lettings_site.Address/Letting` n’existent plus dans
   les schémas récents.  Pour maintenir l’historique tout en permettant la
   création d’une base de test from-scratch, on transforme la migration en
   NO-OP (aucune opération).
"""

from django.db import migrations


def noop(apps, schema_editor):
    """Ne fait rien (legacy data déjà migrée ou inexistante)."""
    # On laisse la fonction vide ; plus de LookupError.
    return


class Migration(migrations.Migration):
    dependencies = [
        ("lettings", "0001_initial"),
        # On garde la dépendance vers la vieille app si elle existe encore ;
        # sinon Django l’ignore.
        ("oc_lettings_site", "0001_initial"),
    ]

    # Migration sautée lors de `migrate --plan` (prod) ET ignorée en tests
    elidable = True

    operations = [
        migrations.RunPython(noop, noop),
    ]
