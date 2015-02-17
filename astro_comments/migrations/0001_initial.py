# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_comments', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomComment',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_comments.Comment')),
            ],
            options={
                'ordering': ['-submit_date'],
            },
            bases=('django_comments.comment',),
        ),
    ]
