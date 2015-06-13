# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0019_auto_20150611_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='solarsystemobject',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
