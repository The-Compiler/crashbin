from django.db import migrations
from django.conf import settings


def create_mailbox(apps, schema_editor):
    Mailbox = apps.get_model('django_mailbox', 'Mailbox')
    Mailbox.objects.create(name='crashbin inbox',
                           uri=settings.CRASHBIN_CONFIG.EMAIL['incoming_url'])


class Migration(migrations.Migration):

    dependencies = [
        ('crashbin_app', '0007_merge_20190514_1406'),
    ]

    operations = [
        migrations.RunPython(create_mailbox)
    ]
