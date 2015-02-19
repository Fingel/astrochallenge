# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150219_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='altitude',
            new_name='elevation',
        ),
    ]
