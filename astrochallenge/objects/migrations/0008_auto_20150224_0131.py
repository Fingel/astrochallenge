# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0007_auto_20150224_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solarsystemobject',
            name='mass_unit',
            field=models.CharField(default=b'e', max_length=1, choices=[(b's', b'solar mass'), (b'e', b'earth mass'), (b'j', b'jupiter mass')]),
            preserve_default=True,
        ),
    ]
