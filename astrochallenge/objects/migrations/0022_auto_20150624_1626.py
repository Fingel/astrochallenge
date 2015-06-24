# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0021_supernova_supernovamagnitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supernova',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
