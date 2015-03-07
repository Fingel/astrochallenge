# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0008_auto_20150224_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solarsystemobject',
            name='mass_unit',
            field=models.CharField(default=b'e', max_length=5, choices=[(b's', b's'), (b'e', b'e'), (b'j', b'j'), (b'kg', b'kg')]),
            preserve_default=True,
        ),
    ]
