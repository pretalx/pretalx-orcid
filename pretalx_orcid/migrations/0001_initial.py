# Generated by Django 2.2.7 on 2019-11-20 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OrcidProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("orcid", models.CharField(blank=True, max_length=40, null=True)),
                (
                    "access_token",
                    models.CharField(blank=True, max_length=40, null=True),
                ),
                (
                    "refresh_token",
                    models.CharField(blank=True, max_length=40, null=True),
                ),
                ("scope", models.CharField(blank=True, max_length=40, null=True)),
                ("expires_in", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orcid_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
