# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0026_auto_20150707_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='solarsystemobject',
            name='magnitude',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
