# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0004_auto_20151009_2300'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentTestCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('case_input', models.TextField(max_length=8096, blank=True)),
                ('case_output', models.TextField(max_length=8096, blank=True)),
                ('max_memory_usage', models.PositiveSmallIntegerField(default=0)),
                ('max_cpu_usage', models.PositiveSmallIntegerField(default=0)),
                ('flags', models.TextField(max_length=1024, blank=True)),
                ('assignment', models.ForeignKey(to='assignments.CourseAssignment', related_name='testcases')),
            ],
        ),
    ]
