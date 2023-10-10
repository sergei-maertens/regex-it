# Generated by Django 3.2.21 on 2023-10-02 07:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0002_expensesconfiguration"),
    ]

    operations = [
        migrations.AddField(
            model_name="expensesconfiguration",
            name="tmobile_creditor",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="expenses.creditor",
                verbose_name="T-Mmobile creditor",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="md5_hash",
            field=models.CharField(
                blank=True, max_length=32, verbose_name="MD5 file hash"
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="notes",
            field=models.TextField(blank=True, verbose_name="notes"),
        ),
        migrations.AddField(
            model_name="invoice",
            name="review_required",
            field=models.BooleanField(
                default=False, verbose_name="manual review required"
            ),
        ),
    ]
