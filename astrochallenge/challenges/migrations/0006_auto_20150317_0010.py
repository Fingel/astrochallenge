# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_auto_20150316_2210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='completedchallenge',
            options={'ordering': ['-date']},
        ),
    ]
