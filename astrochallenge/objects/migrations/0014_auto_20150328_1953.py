# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0013_auto_20150328_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='astroobject',
            name='image_attribution',
            field=models.CharField(default=b'', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solarsystemobject',
            name='image_attribution',
            field=models.CharField(default=b'', max_length=1000, blank=True),
            preserve_default=True,
        ),
    ]
