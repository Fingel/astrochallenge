# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0012_auto_20150310_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='astroobject',
            name='image_attribution',
            field=models.CharField(default=b'', max_length=1000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='solarsystemobject',
            name='image_attribution',
            field=models.CharField(default=b'', max_length=1000),
            preserve_default=True,
        ),
    ]
