# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_equipment'),
        ('objects', '0012_auto_20150310_0738'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.CharField(max_length=1, choices=[(b'A', b'astroobject'), (b'S', b'solarsystemobject'), (b'C', b'composite')])),
                ('name', models.CharField(max_length=200)),
                ('multiplier', models.IntegerField(default=1)),
                ('bonus', models.IntegerField(default=0)),
                ('complete_bonus', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('image', models.ImageField(null=True, upload_to=b'challenges', blank=True)),
                ('astroobjects', models.ManyToManyField(to='objects.AstroObject', null=True, blank=True)),
                ('solarsystemobjects', models.ManyToManyField(to='objects.SolarSystemObject', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompletedChallenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('challenge', models.ForeignKey(to='challenges.Challenge')),
                ('user_profile', models.ForeignKey(to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NumericalChallenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.CharField(max_length=1, choices=[(b'A', b'astroobject'), (b'S', b'solarsystemobject'), (b'C', b'composite')])),
                ('number', models.PositiveIntegerField(default=1)),
                ('complete_bonus', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
