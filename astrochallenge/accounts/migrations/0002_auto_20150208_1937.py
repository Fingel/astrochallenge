# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email_verified',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default=b'UTC'),
            preserve_default=True,
        ),
    ]
