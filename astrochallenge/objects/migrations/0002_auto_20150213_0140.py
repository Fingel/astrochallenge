# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogobject',
            name='catalog',
            field=models.CharField(max_length=200, choices=[(b'C', b'Caldwell'), (b'M', b'Messier'), (b'NGC', b'NGC')]),
            preserve_default=True,
        ),
    ]
