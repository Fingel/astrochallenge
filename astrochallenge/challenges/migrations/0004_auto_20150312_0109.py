# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_auto_20150311_2336'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NumericalChallenge',
        ),
        migrations.AddField(
            model_name='challenge',
            name='number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='challenge',
            name='type',
            field=models.CharField(default='set', max_length=200, choices=[(b'set', b'set'), (b'numeric', b'numeric')]),
            preserve_default=False,
        ),
    ]
