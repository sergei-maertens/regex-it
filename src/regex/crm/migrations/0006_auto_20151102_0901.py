# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20151021_0900'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'project', 'verbose_name_plural': 'projects'},
        ),
        migrations.AddField(
            model_name='client',
            name='language',
            field=models.CharField(default='nl', choices=[('nl', 'Dutch'), ('nl_BE', 'Dutch (Belgium)')], verbose_name='language', max_length=10),
        ),
    ]
