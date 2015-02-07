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
                ('ra', models.DecimalField(max_digits=10, decimal_places=7)),
                ('dec', models.DecimalField(max_digits=10, decimal_places=7)),
                ('magnitude', models.DecimalField(max_digits=4, decimal_places=2)),
                ('distance', models.IntegerField(default=0)),
                ('size', models.DecimalField(max_digits=5, decimal_places=3)),
                ('constellation', models.CharField(max_length=200, blank=True)),
                ('detailed_type', models.CharField(max_length=200, blank=True)),
                ('common_name', models.CharField(max_length=200, blank=True)),
                ('points', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to=b'astro_objects', blank=True)),
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
    ]
