# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='generated',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateField(help_text='Include work up to (including) this day.', verbose_name='date'),
        ),
    ]
