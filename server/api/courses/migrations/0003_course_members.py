# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course'),
        ('members', '0002_auto_20151009_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='members',
            field=models.ManyToManyField(to='members.Member', related_name='courses', through='members.Membership'),
        ),
    ]
