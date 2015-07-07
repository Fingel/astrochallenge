# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0012_challenge_supernovae'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='short_name',
            field=models.CharField(default=b'', max_length=50, blank=True),
        ),
    ]
