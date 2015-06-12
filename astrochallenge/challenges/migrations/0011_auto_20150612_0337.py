# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0010_auto_20150328_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='astroobjects',
            field=models.ManyToManyField(to='objects.AstroObject', blank=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='solarsystemobjects',
            field=models.ManyToManyField(to='objects.SolarSystemObject', blank=True),
        ),
    ]
