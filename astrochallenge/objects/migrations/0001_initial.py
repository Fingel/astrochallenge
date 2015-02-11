# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AstroObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=200)),
                ('ra_hours', models.IntegerField(null=True, blank=True)),
                ('ra_minutes', models.FloatField(null=True, blank=True)),
                ('dec_sign', models.CharField(default=b'', max_length=1, blank=True, choices=[(b'+', b'+'), (b'-', b'-')])),
                ('dec_deg', models.IntegerField(null=True, blank=True)),
                ('dec_min', models.FloatField(null=True, blank=True)),
                ('magnitude', models.FloatField(null=True, blank=True)),
                ('size', models.FloatField(null=True, blank=True)),
                ('distance', models.FloatField(null=True, blank=True)),
                ('details', models.CharField(default=b'', max_length=200, blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
                ('common_name', models.CharField(default=b'', max_length=200, blank=True)),
                ('points', models.IntegerField(default=0)),
                ('image', models.ImageField(null=True, upload_to=b'astro_objects', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CatalogObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('catalog', models.CharField(max_length=200, choices=[(b'M', b'Messier'), (b'NGC', b'NGC'), (b'C', b'Caldwell')])),
                ('designation', models.CharField(max_length=50)),
                ('astro_object', models.ForeignKey(to='objects.AstroObject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Constellation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(unique=True, max_length=3)),
                ('latin_name', models.CharField(max_length=200)),
                ('latin_genitive', models.CharField(max_length=200)),
                ('english_name', models.CharField(max_length=200)),
                ('image', models.ImageField(null=True, upload_to=b'constellations', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='catalogobject',
            unique_together=set([('catalog', 'designation')]),
        ),
        migrations.AddField(
            model_name='astroobject',
            name='constellation',
            field=models.ForeignKey(blank=True, to='objects.Constellation', null=True),
            preserve_default=True,
        ),
    ]
