# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0014_auto_20150328_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='astroobject',
            name='dec_seconds',
            field=models.FloatField(default=0.0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='astroobject',
            name='ra_seconds',
            field=models.FloatField(default=0.0, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='catalogobject',
            name='catalog',
            field=models.CharField(max_length=200, choices=[(b'HIP', b'Hipparcos'), (b'C', b'Caldwell'), (b'M', b'Messier'), (b'HD', b'Henry Draper'), (b'NGC', b'NGC')]),
            preserve_default=True,
        ),
    ]
