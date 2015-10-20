# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import regex.utils.storages
import re


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20151005_2300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoiceitem',
            options={'verbose_name': 'invoice item', 'verbose_name_plural': 'invoice items'},
        ),
        migrations.AddField(
            model_name='invoice',
            name='pdf',
            field=models.FileField(blank=True, storage=regex.utils.storages.PrivateMediaFileSystemStorage, verbose_name='pdf', upload_to='invoices/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(unique=True, verbose_name='invoice number', validators=[django.core.validators.RegexValidator(re.compile('(?P<year>20\\d{2})\\d{5}$', 32))], default=None, blank=True, null=True, max_length=50),
        ),
    ]
