# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20150924_1717'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date', models.DateField(verbose_name='date')),
                ('due_date', models.DateTimeField(verbose_name='due date', blank=True, null=True)),
                ('received', models.DateTimeField(verbose_name='received', blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('client', models.ForeignKey(to='crm.Client')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('rate', models.DecimalField(verbose_name='rate', decimal_places=2, max_digits=10)),
                ('amount', models.DecimalField(verbose_name='amount', decimal_places=2, max_digits=10)),
                ('tax_rate', models.DecimalField(verbose_name='tax rate', decimal_places=2, choices=[(Decimal('0.06'), 'low'), (Decimal('0.21'), 'high')], max_digits=4, default=Decimal('0.21'))),
                ('object_id', models.IntegerField(blank=True, null=True)),
                ('remarks', models.TextField(verbose_name='remarks', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', blank=True, null=True)),
                ('invoice', models.ForeignKey(to='invoices.Invoice')),
                ('project', models.ForeignKey(to='crm.Project', blank=True, null=True)),
            ],
        ),
    ]
