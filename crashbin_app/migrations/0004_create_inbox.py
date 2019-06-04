from django.db import migrations


def create_inbox(apps, schema_editor):
    Bin = apps.get_model("crashbin_app", "Bin")
    Bin.objects.create(name="Inbox", description="Default inbox bin for new reports.")


class Migration(migrations.Migration):

    dependencies = [("crashbin_app", "0003_related_name")]

    operations = [migrations.RunPython(create_inbox)]
