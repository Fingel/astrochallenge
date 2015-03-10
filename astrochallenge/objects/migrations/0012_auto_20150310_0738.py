# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0011_auto_20150310_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='light_pollution',
            field=models.CharField(default=b'A', max_length=2, choices=[(b'P', b'poor'), (b'BA', b'below average'), (b'A', b'average'), (b'AA', b'above average'), (b'E', b'excellent')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='observation',
            name='seeing',
            field=models.CharField(default=b'A', max_length=2, choices=[(b'P', b'poor'), (b'BA', b'below average'), (b'A', b'average'), (b'AA', b'above average'), (b'E', b'excellent')]),
            preserve_default=True,
        ),
    ]
