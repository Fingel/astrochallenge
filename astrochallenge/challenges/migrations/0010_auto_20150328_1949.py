# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0009_auto_20150320_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='target',
            field=models.CharField(max_length=200, choices=[(b'astro object', b'astro object'), (b'solar system object', b'solar system object'), (b'composite', b'solar system or deep space object')]),
            preserve_default=True,
        ),
    ]
