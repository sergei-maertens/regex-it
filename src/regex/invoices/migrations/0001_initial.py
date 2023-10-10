# Generated by Django 2.2.7 on 2019-11-17 14:39

import re
from decimal import Decimal

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

from privates.fields import PrivateMediaFileField


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("crm", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
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
                (
                    "date",
                    models.DateField(
                        help_text="Include work up to (including) this day.",
                        verbose_name="date",
                    ),
                ),
                ("generated", models.DateTimeField(editable=False, null=True)),
                (
                    "invoice_number",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=50,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("(?P<year>20\\d{2})\\d{5}$")
                            )
                        ],
                        verbose_name="invoice number",
                    ),
                ),
                (
                    "due_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="due date"
                    ),
                ),
                (
                    "pdf",
                    PrivateMediaFileField(
                        blank=True, upload_to="invoices/%Y/%m", verbose_name="pdf"
                    ),
                ),
                (
                    "received",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="received"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="crm.Client"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InvoiceItem",
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
                (
                    "rate",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="rate"
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="amount"
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
                ("object_id", models.IntegerField(blank=True, null=True)),
                ("remarks", models.TextField(blank=True, verbose_name="remarks")),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="invoices.Invoice",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="crm.Project",
                    ),
                ),
            ],
            options={
                "verbose_name": "invoice item",
                "verbose_name_plural": "invoice items",
            },
        ),
    ]
