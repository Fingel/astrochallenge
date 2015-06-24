# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0022_auto_20150624_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supernova',
            name='astro_object',
            field=models.ForeignKey(default=None, blank=True, to='objects.AstroObject', null=True),
        ),
    ]
