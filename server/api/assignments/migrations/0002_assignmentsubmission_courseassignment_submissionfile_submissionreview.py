# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid
import api.assignments.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('pull_request', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('grade', models.PositiveSmallIntegerField(default=0)),
                ('description', models.CharField(max_length=256, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=48)),
                ('description', models.TextField()),
                ('assignment_type', models.CharField(max_length=1, default='H', choices=[('H', 'Homework'), ('E', 'Exam'), ('P', 'Practice')])),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField()),
                ('target', models.CharField(max_length=3, default='ALL', choices=[('A', 'A class'), ('B', 'B class'), ('V', 'V class'), ('G', 'G class'), ('ALL', 'ALL classes')])),
                ('code', models.CharField(max_length=200, editable=False, default=uuid.uuid4)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('file', models.FileField(upload_to=api.assignments.models.SubmissionFile.generate_filename)),
                ('sha', models.CharField(max_length=1024)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionReview',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('description', models.TextField()),
                ('points', models.PositiveSmallIntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
