# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0020_solarsystemobject_date_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supernova',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('ra_hours', models.IntegerField()),
                ('ra_minutes', models.FloatField()),
                ('ra_seconds', models.FloatField(default=0.0, blank=True)),
                ('dec_sign', models.CharField(default=b'+', max_length=1, choices=[(b'+', b'+'), (b'-', b'-')])),
                ('dec_deg', models.IntegerField()),
                ('dec_min', models.FloatField()),
                ('dec_seconds', models.FloatField(default=0.0, blank=True)),
                ('discovery_date', models.DateTimeField()),
                ('sntype', models.CharField(max_length=255)),
                ('z', models.FloatField(null=True, blank=True)),
                ('astro_object', models.ForeignKey(to='objects.AstroObject')),
            ],
        ),
        migrations.CreateModel(
            name='SupernovaMagnitude',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('magnitude', models.FloatField()),
                ('time', models.DateTimeField()),
                ('supernova', models.ForeignKey(to='objects.Supernova')),
            ],
        ),
    ]
