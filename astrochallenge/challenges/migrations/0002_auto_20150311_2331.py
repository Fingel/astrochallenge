# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='target',
            field=models.CharField(max_length=200, choices=[(b'astro object', b'astro object'), (b'solar ststem object', b'solar system object'), (b'composite', b'composite')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='numericalchallenge',
            name='target',
            field=models.CharField(max_length=200, choices=[(b'astro object', b'astro object'), (b'solar ststem object', b'solar system object'), (b'composite', b'composite')]),
            preserve_default=True,
        ),
    ]
