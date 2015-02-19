# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150213_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='altitude',
            field=models.IntegerField(default=0, help_text=b'The elevation, in meters, from which you most often observe from.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lat',
            field=models.FloatField(default=0.0, help_text=b'The latitude form which you most often observe from.', verbose_name=b'latitude'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lng',
            field=models.FloatField(default=0.0, help_text=b'The longitude from which you most often observe from.', verbose_name=b'longitude'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(default=b'', help_text=b'Doesn\'t need to be accurate, just a description of your location. e.g "San Francisco"', max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
