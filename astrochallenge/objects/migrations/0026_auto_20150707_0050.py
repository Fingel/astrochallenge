# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0025_supernova_date_added'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supernovamagnitude',
            options={'ordering': ('time',)},
        ),
    ]
