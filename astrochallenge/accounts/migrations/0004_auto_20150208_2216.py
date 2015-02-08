# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150208_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='lat',
            field=models.DecimalField(verbose_name=b'latitude', max_digits=10, decimal_places=7),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lng',
            field=models.DecimalField(verbose_name=b'longitude', max_digits=10, decimal_places=7),
            preserve_default=True,
        ),
    ]
