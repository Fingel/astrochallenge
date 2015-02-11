# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timezone', timezone_field.fields.TimeZoneField(default=b'UTC')),
                ('location', models.CharField(default=b'', max_length=200, blank=True)),
                ('lat', models.DecimalField(null=True, verbose_name=b'latitude', max_digits=10, decimal_places=7, blank=True)),
                ('lng', models.DecimalField(null=True, verbose_name=b'longitude', max_digits=10, decimal_places=7, blank=True)),
                ('profile_text', models.TextField(default=b'', blank=True)),
                ('user', models.OneToOneField(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
