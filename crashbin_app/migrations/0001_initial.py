# Generated by Django 2.2 on 2019-04-09 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Label",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("color", models.CharField(max_length=7)),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="Bin",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("labels", models.ManyToManyField(blank=True, to="crashbin_app.Label")),
                (
                    "maintainers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="maintained_bins",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "related_bins",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_bin_related_bins_+",
                        to="crashbin_app.Bin",
                    ),
                ),
                (
                    "subscribers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="subscribed_bins",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "bin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crashbin_app.Bin",
                    ),
                ),
                ("labels", models.ManyToManyField(blank=True, to="crashbin_app.Label")),
                ("log", models.TextField(blank=True)),
            ],
        ),
    ]
