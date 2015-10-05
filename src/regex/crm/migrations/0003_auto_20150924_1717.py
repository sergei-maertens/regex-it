# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20150924_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='flat_fee',
            field=models.DecimalField(verbose_name='flat fee', decimal_places=2, null=True, max_digits=10, blank=True),
        ),
    ]
