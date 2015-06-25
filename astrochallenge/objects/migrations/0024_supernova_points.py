# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0023_auto_20150624_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='supernova',
            name='points',
            field=models.IntegerField(default=10),
        ),
    ]
