# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0015_auto_20150406_1835'),
        ('accounts', '0005_equipment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kudos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('observation', models.ForeignKey(to='objects.Observation')),
                ('user_profile', models.ForeignKey(to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
