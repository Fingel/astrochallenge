# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0006_auto_20150219_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolarSystemObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=50, choices=[(b'P', b'planet'), (b'MP', b'minor planet'), (b'M', b'moon'), (b'A', b'asteroid'), (b'C', b'comet'), (b'S', b'satellite'), (b'SC', b'spacecraft'), (b'ST', b'star')])),
                ('index', models.IntegerField(default=999999)),
                ('ephemeride', models.CharField(default=b'', max_length=1000)),
                ('description', models.TextField(default=b'')),
                ('mass', models.FloatField(null=True, blank=True)),
                ('mass_unit', models.CharField(default=b'e', max_length=1, choices=[(b's', b's'), (b'e', b'e'), (b'j', b'j')])),
                ('points', models.IntegerField(default=0)),
                ('image', models.ImageField(null=True, upload_to=b'ss_objects', blank=True)),
                ('parent', models.ForeignKey(blank=True, to='objects.SolarSystemObject', null=True)),
            ],
            options={
                'ordering': ['index'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='astroobject',
            options={'ordering': ['index']},
        ),
        migrations.AddField(
            model_name='astroobject',
            name='index',
            field=models.IntegerField(default=999999),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='dec_deg',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='dec_min',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='dec_sign',
            field=models.CharField(default=b'+', max_length=1, choices=[(b'+', b'+'), (b'-', b'-')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='ra_hours',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='astroobject',
            name='ra_minutes',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
