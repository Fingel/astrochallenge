# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150208_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='lat',
            field=models.DecimalField(null=True, verbose_name=b'latitude', max_digits=10, decimal_places=7, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lng',
            field=models.DecimalField(null=True, verbose_name=b'longitude', max_digits=10, decimal_places=7, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_text',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
