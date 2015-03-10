# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0009_auto_20150307_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solarsystemobject',
            name='type',
            field=models.CharField(max_length=50, choices=[(b'P', b'planet'), (b'DP', b'dwarf planet'), (b'M', b'moon'), (b'A', b'asteroid'), (b'C', b'comet'), (b'S', b'satellite'), (b'SC', b'spacecraft'), (b'ST', b'star')]),
            preserve_default=True,
        ),
    ]
