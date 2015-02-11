# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0003_auto_20150211_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='astroobject',
            old_name='ra_sign',
            new_name='dec_sign',
        ),
    ]
