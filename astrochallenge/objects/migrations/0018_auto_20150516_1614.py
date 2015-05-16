# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0017_auto_20150412_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='astroobject',
            name='discoverer',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='astroobject',
            name='discovery_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
