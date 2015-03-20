# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0008_auto_20150320_0022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challenge',
            options={'ordering': ['index', 'rating']},
        ),
        migrations.AddField(
            model_name='challenge',
            name='index',
            field=models.PositiveIntegerField(default=9999),
            preserve_default=True,
        ),
    ]
