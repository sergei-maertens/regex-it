# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_auto_20151005_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(max_length=50, default='', verbose_name='invoice number', unique=True),
            preserve_default=False,
        ),
    ]
