# Generated by Django 3.2.21 on 2023-10-02 07:13

import hashlib

from django.db import migrations


def set_hashes(apps, _):
    Invoice = apps.get_model("expenses", "Invoice")
    for invoice in Invoice.objects.exclude(pdf="").filter(md5_hash=""):
        with invoice.pdf.open("rb") as infile:
            md5_hash = hashlib.md5(infile.read()).hexdigest()
        invoice.md5_hash = md5_hash
        invoice.save()


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0003_auto_20231002_0906"),
    ]

    operations = [
        migrations.RunPython(set_hashes, migrations.RunPython.noop),
    ]