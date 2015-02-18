# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0004_auto_20150217_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='lat',
            field=models.FloatField(default=0.0, verbose_name=b'latitude'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='observation',
            name='lng',
            field=models.FloatField(default=0.0, verbose_name=b'longitude'),
            preserve_default=True,
        ),
    ]
