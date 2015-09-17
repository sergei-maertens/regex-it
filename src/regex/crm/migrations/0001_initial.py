# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', autoslug.fields.AutoSlugField(unique=True, populate_from='name', editable=False, verbose_name='slug')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('city', models.CharField(max_length=255, verbose_name='city')),
                ('country', django_countries.fields.CountryField(default='NL', max_length=2, verbose_name='Country')),
                ('crn', models.CharField(max_length=50, blank=True, help_text='KvK number', verbose_name='registration number')),
                ('vat', models.CharField(max_length=50, blank=True, verbose_name='VAT number')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'verbose_name_plural': 'clients',
                'verbose_name': 'client',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('label', models.CharField(max_length=50, verbose_name='label')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('address', models.CharField(max_length=255, blank=True, verbose_name='address')),
                ('postal_code', models.CharField(max_length=10, verbose_name='postal code')),
                ('city', models.CharField(max_length=255, verbose_name='city')),
                ('country', django_countries.fields.CountryField(default='NL', max_length=2, verbose_name='Country')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'contacts',
                'verbose_name': 'contact',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='contacts',
            field=models.ManyToManyField(to='crm.Contact', blank=True),
        ),
    ]
