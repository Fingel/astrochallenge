# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150213_2008'),
        ('contenttypes', '0001_initial'),
        ('objects', '0002_auto_20150213_0140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('points_earned', models.PositiveIntegerField(default=0, editable=False)),
                ('description', models.TextField(default=b'', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user_profile', models.ForeignKey(to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
