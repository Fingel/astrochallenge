# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0005_auto_20150218_0148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='observation',
            options={'ordering': ['-date']},
        ),
    ]
