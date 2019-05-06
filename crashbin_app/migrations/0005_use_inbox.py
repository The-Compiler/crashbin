# Generated by Django 2.2.1 on 2019-05-06 13:30

import crashbin_app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crashbin_app', '0004_create_inbox'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='bin',
            field=models.ForeignKey(default=crashbin_app.models.Bin.get_inbox, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='crashbin_app.Bin'),
        ),
    ]