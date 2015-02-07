# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='astroobject',
            name='size',
            field=models.DecimalField(max_digits=7, decimal_places=3),
            preserve_default=True,
        ),
    ]
