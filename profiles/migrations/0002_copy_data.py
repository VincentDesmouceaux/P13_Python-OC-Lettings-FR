# profiles/migrations/0002_copy_data.py
from django.db import migrations


def noop(apps, schema_editor):
    """
    Fonction neutre pour les opérations de migration.
    Historiquement, cette migration était destinée à copier les données depuis
    l'ancienne application 'profiles'. Après refactoring, cette opération n'est plus nécessaire.
    Cette fonction ne fait rien et est utilisée comme placeholder pour maintenir
    la cohérence du système de migration.
    """
    return


class Migration(migrations.Migration):
    """
    Migration de copie de données (devenue obsolète).
    Cette migration était initialement prévue pour transférer les données depuis
    l'ancienne implémentation du profil utilisateur. Après refactoring de l'application,
    cette opération n'est plus nécessaire.
    Caractéristiques:
    - Marqué comme 'elidable': Cette migration peut être supprimée lors du squash des migrations
    - Opération neutre: La fonction noop est exécutée à la place des opérations de copie
    Dépendances:
    - Dépend de la migration initiale (0001_initial)
    """

    dependencies = [
        ("profiles", "0001_initial"),
    ]
    # Permet de supprimer cette migration lors du squash
    elidable = True
    operations = [
        # Opération neutre (ne fait rien)
        migrations.RunPython(noop, noop)
    ]
