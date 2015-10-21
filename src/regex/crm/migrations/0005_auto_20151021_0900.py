# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_client_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='base_rate',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='hourly base rate', blank=True),
        ),
    ]
