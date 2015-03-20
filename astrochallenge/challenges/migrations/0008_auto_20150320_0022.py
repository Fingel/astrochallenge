# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0007_auto_20150317_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='target',
            field=models.CharField(max_length=200, choices=[(b'astro object', b'astro object'), (b'solar ststem object', b'solar system object'), (b'composite', b'solar system or deep space object')]),
            preserve_default=True,
        ),
    ]
