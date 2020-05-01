# Generated by Django 2.2.12 on 2020-04-25 15:20
import os

from django.db import migrations

VALUES = {
    "company_name": os.getenv("COMPANY_NAME"),
    "company_address": (os.getenv("COMPANY_ADDRESS") or "").split(","),
    "tax_identifier": os.getenv("COMPANY_TAX_IDENTIFIER"),
    "coc": os.getenv("COMPANY_KVK"),
    "iban": os.getenv("COMPANY_IBAN"),
}


def set_values_from_env(apps, _):
    from ..models import CompanyConfig as RealCompanyConfig

    CompanyConfig = apps.get_model("config", "CompanyConfig")

    config, created = CompanyConfig.objects.get_or_create(
        pk=RealCompanyConfig.singleton_instance_id
    )
    for field, value in VALUES.items():
        if not getattr(config, field):
            setattr(config, field, value)
    config.save()


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(set_values_from_env, migrations.RunPython.noop),
    ]
