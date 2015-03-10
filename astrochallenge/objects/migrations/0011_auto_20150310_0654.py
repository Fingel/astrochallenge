# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_equipment'),
        ('objects', '0010_auto_20150310_0555'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='equipment',
            field=models.ForeignKey(blank=True, to='accounts.Equipment', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='observation',
            name='light_pollution',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='observation',
            name='seeing',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
