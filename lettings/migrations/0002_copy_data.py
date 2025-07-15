# lettings/migrations/0002_copy_data.py
"""
Migration de copie de données legacy neutralisée
Contexte historique:
- À l'origine, cette migration copiait les données des anciens modèles 
  `oc_lettings_site.Address` et `oc_lettings_site.Letting` vers les nouveaux 
  modèles `lettings.Address` et `lettings.Letting`
- Les anciens modèles n'existent plus dans les schémas actuels
État actuel:
- Transformée en NO-OP (aucune opération) pour:
  1. Maintenir l'historique des migrations
  2. Permettre la création de bases de test from-scratch
  3. Éviter les erreurs de lookup sur des modèles disparus
Comportement:
- Les fonctions de migration (avance et recul) sont vides (noop)
- Élidable: Exclue automatiquement lors de `migrate --plan`
- Ignorée dans les environnements de test
Dépendances:
- lettings.0001_initial (nouveaux modèles)
- oc_lettings_site.0001_initial (ancienne app, tolérée si absente)
Important:
- Ne doit plus être exécutée en production (les données legacy ont déjà migré)
- Préservée pour l'intégrité de l'historique des migrations
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
