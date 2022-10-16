# Generated by Django 2.2.7 on 2019-11-17 14:39

from decimal import Decimal

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import autoslug.fields
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=50, verbose_name="label")),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                ("email", models.EmailField(max_length=254, verbose_name="email")),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="phone number"
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="address"
                    ),
                ),
                (
                    "postal_code",
                    models.CharField(
                        blank=True, max_length=10, verbose_name="postal code"
                    ),
                ),
                (
                    "city",
                    models.CharField(blank=True, max_length=255, verbose_name="city"),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="NL", max_length=2, verbose_name="Country"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "contact",
                "verbose_name_plural": "contacts",
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from="name",
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="email")),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="phone number"
                    ),
                ),
                ("address", models.CharField(max_length=255, verbose_name="address")),
                ("city", models.CharField(max_length=255, verbose_name="city")),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="NL", max_length=2, verbose_name="Country"
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("en", "English"),
                            ("nl", "Dutch"),
                            ("nl_BE", "Dutch (Belgium)"),
                        ],
                        default="nl",
                        max_length=10,
                        verbose_name="language",
                    ),
                ),
                (
                    "crn",
                    models.CharField(
                        blank=True,
                        help_text="KvK number",
                        max_length=50,
                        verbose_name="registration number",
                    ),
                ),
                (
                    "vat",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="VAT number"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                ("contacts", models.ManyToManyField(blank=True, to="crm.Contact")),
            ],
            options={
                "verbose_name": "client",
                "verbose_name_plural": "clients",
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(editable=False, populate_from="name"),
                ),
                (
                    "base_rate",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=8,
                        null=True,
                        verbose_name="hourly base rate",
                    ),
                ),
                (
                    "flat_fee",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="flat fee",
                    ),
                ),
                (
                    "tax_rate",
                    models.DecimalField(
                        choices=[(Decimal("0.06"), "low"), (Decimal("0.21"), "high")],
                        decimal_places=2,
                        default=Decimal("0.21"),
                        max_digits=4,
                        verbose_name="tax rate",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="crm.Client"
                    ),
                ),
            ],
            options={
                "verbose_name": "project",
                "verbose_name_plural": "projects",
                "unique_together": {("client", "slug")},
            },
        ),
    ]
