# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import autoslug.fields


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        serialize=False,
                        verbose_name="ID",
                        primary_key=True,
                        auto_created=True,
                    ),
                ),
                ("name", models.CharField(verbose_name="name", max_length=255)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from="name",
                        verbose_name="slug",
                        unique=True,
                    ),
                ),
                (
                    "image",
                    models.ImageField(blank=True, verbose_name="image", upload_to=""),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "published",
                    models.BooleanField(verbose_name="published", default=False),
                ),
            ],
            options={
                "verbose_name": "portfolio entry",
                "verbose_name_plural": "portfolio entries",
                "ordering": ["order"],
            },
        ),
    ]
