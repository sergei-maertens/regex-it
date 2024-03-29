# Generated by Django 3.2.16 on 2022-10-15 17:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="language",
            field=models.CharField(
                choices=[
                    ("en", "English"),
                    ("nl", "Dutch"),
                    ("nl-be", "Dutch (Belgium)"),
                ],
                default="nl",
                max_length=10,
                verbose_name="language",
            ),
        ),
    ]
