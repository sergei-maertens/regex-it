# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False)),
                ('base_rate', models.DecimalField(verbose_name='hourly base rate', decimal_places=2, max_digits=8)),
                ('flat_fee', models.DecimalField(verbose_name='flat fee', decimal_places=2, max_digits=10)),
                ('tax_rate', models.DecimalField(choices=[(Decimal('0.06'), 'low'), (Decimal('0.21'), 'high')], verbose_name='tax rate', decimal_places=2, max_digits=4, default=Decimal('0.21'))),
                ('client', models.ForeignKey(to='crm.Client')),
            ],
        ),
        migrations.AlterField(
            model_name='contact',
            name='city',
            field=models.CharField(verbose_name='city', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='postal_code',
            field=models.CharField(verbose_name='postal code', max_length=10, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('client', 'slug')]),
        ),
    ]
