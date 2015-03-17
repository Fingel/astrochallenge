# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_auto_20150312_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='description',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='challenge',
            name='rating',
            field=models.PositiveIntegerField(default=3, choices=[(1, b'trivial'), (2, b'easy'), (3, b'moderate'), (4, b'difficult'), (5, b'extremely difficult')]),
            preserve_default=True,
        ),
    ]
