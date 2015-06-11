# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0018_auto_20150516_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogobject',
            name='catalog',
            field=models.CharField(max_length=200, choices=[(b'HIP', b'Hipparcos'), (b'C', b'Caldwell'), (b'NGC', b'NGC'), (b'M', b'Messier'), (b'IC', b'Index Catalog'), (b'HD', b'Henry Draper')]),
        ),
    ]
