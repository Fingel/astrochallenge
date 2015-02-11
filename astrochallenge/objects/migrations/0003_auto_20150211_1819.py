# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0002_auto_20150207_0332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='astroobject',
            name='dec',
        ),
        migrations.RemoveField(
            model_name='astroobject',
            name='detailed_type',
        ),
        migrations.RemoveField(
            model_name='astroobject',
            name='ra',
        ),
        migrations.AddField(
            model_name='astroobject',
            name='dec_deg',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='astroobject',
            name='dec_min',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='astroobject',
            name='description',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='astroobject',
            name='details',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='astroobject',
            name='ra_hours',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='astroobject',
            name='ra_minutes',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='astroobject',
            name='ra_sign',
            field=models.CharField(default=b'', max_length=1, blank=True, choices=[(b'+', b'+'), (b'-', b'-')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='common_name',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='constellation',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='distance',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='image',
            field=models.ImageField(null=True, upload_to=b'astro_objects', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='magnitude',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='size',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
