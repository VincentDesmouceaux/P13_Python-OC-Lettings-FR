from django.db import migrations


def forwards(apps, schema_editor):
    OldProfile = apps.get_model("oc_lettings_site", "Profile")
    NewProfile = apps.get_model("profiles", "Profile")

    for old in OldProfile.objects.all():
        NewProfile.objects.create(user_id=old.user_id, favorite_city=old.favorite_city)


class Migration(migrations.Migration):
    dependencies = [("profiles", "0001_initial")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
