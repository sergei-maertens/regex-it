# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_invoice_invoice_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(null=True, max_length=50, default=None, verbose_name='invoice number', unique=True, blank=True),
        ),
    ]
