# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0015_auto_20150406_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='image',
            field=models.ImageField(help_text=b'Maximum file size: 50mb. You can display additional images in your observation by hosting them elsewhere and linking to them using the picture button.', null=True, upload_to=b'observations', blank=True),
            preserve_default=True,
        ),
    ]
