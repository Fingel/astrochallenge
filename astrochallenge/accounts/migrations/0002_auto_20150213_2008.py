# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='lat',
            field=models.FloatField(default=0.0, verbose_name=b'latitude'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lng',
            field=models.FloatField(default=0.0, verbose_name=b'longitude'),
            preserve_default=True,
        ),
    ]
