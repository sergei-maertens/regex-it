# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-19 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entry",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="portfolio", verbose_name="image"
            ),
        ),
    ]
