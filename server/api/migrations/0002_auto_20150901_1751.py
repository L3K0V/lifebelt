# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='role',
        ),
        migrations.AddField(
            model_name='member',
            name='student_class',
            field=models.CharField(null=True, blank=True, choices=[('A', 'A'), ('B', 'B'), ('V', 'V'), ('G', 'G')], max_length=1),
        ),
        migrations.AddField(
            model_name='member',
            name='student_grade',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='student_number',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='role',
            field=models.CharField(default='S', choices=[('S', 'Student'), ('T', 'Teacher')], max_length=1),
        ),
    ]
