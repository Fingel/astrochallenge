# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0003_observation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='observation',
            name='points_earned',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
