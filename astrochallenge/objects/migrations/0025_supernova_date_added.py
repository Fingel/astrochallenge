# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0024_supernova_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='supernova',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
