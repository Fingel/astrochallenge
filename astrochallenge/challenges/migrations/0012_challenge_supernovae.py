# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0025_supernova_date_added'),
        ('challenges', '0011_auto_20150612_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='supernovae',
            field=models.ManyToManyField(to='objects.Supernova', blank=True),
        ),
    ]
