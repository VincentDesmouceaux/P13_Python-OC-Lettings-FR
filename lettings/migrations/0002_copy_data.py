from django.db import migrations


def forwards(apps, schema_editor):
    OldAddress = apps.get_model("oc_lettings_site", "Address")
    OldLetting = apps.get_model("oc_lettings_site", "Letting")
    NewAddress = apps.get_model("lettings", "Address")
    NewLetting = apps.get_model("lettings", "Letting")

    for old_addr in OldAddress.objects.all():
        new_addr = NewAddress.objects.create(
            number=old_addr.number,
            street=old_addr.street,
            city=old_addr.city,
            state=old_addr.state,
            zip_code=old_addr.zip_code,
            country_iso_code=old_addr.country_iso_code,
        )
        old_letting = OldLetting.objects.get(address=old_addr)
        NewLetting.objects.create(title=old_letting.title, address=new_addr)


class Migration(migrations.Migration):
    dependencies = [("lettings", "0001_initial")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
