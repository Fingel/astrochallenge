# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0016_observation_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='featured',
            field=models.BooleanField(default=False, help_text=b'Feature this observation on your profile.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='observation',
            name='image',
            field=models.ImageField(help_text=b'Maximum file size: 50mb.', null=True, upload_to=b'observations', blank=True),
            preserve_default=True,
        ),
    ]
