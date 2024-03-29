# Generated by Django 2.2.7 on 2019-11-17 14:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("crm", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkEntry",
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
                ("start", models.DateTimeField(verbose_name="start")),
                ("end", models.DateTimeField(verbose_name="end")),
                ("notes", models.TextField(blank=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="crm.Project"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "work entry",
                "verbose_name_plural": "work entries",
                "ordering": ("-start",),
            },
        ),
    ]
