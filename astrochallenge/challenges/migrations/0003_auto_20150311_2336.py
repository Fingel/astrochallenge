# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_auto_20150311_2331'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='completedchallenge',
            unique_together=set([('user_profile', 'challenge')]),
        ),
    ]
