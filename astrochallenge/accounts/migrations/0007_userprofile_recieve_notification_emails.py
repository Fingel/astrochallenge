# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_kudos'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='recieve_notification_emails',
            field=models.BooleanField(default=True, help_text=b'Recieve emails when someone gives you kudos or comments on your observations.'),
            preserve_default=True,
        ),
    ]
