# Generated by Django 2.2.1 on 2019-05-20 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("crashbin_app", "0008_create_mailbox")]

    operations = [
        migrations.AlterField(
            model_name="bin",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="label",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
