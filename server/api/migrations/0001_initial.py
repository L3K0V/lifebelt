# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import api.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementComment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('comment', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('pull_request', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('grade', models.PositiveSmallIntegerField(default=0)),
                ('description', models.CharField(blank=True, max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('initials', models.CharField(max_length=16)),
                ('full_name', models.CharField(max_length=48)),
                ('description', models.TextField()),
                ('year', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseAnnouncement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('announcement', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseAssignment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=48)),
                ('description', models.TextField()),
                ('assignment_type', models.CharField(choices=[('H', 'Homework'), ('E', 'Exam'), ('P', 'Practice')], max_length=1, default='H')),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField()),
                ('target', models.CharField(choices=[('A', 'A class'), ('B', 'B class'), ('V', 'V class'), ('G', 'G class'), ('ALL', 'ALL classes')], max_length=3, default='ALL')),
                ('course', models.ForeignKey(related_name='assignments', to='api.Course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('role', models.CharField(choices=[('A', 'Admin'), ('S', 'Student'), ('T', 'Teacher')], max_length=1, default='S')),
                ('github', models.CharField(blank=True, max_length=48)),
                ('github_token', models.CharField(blank=True, max_length=256)),
                ('avatar_url', models.CharField(blank=True, max_length=256)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='member')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('role', models.CharField(choices=[('A', 'Admin'), ('S', 'Student'), ('T', 'Teacher')], max_length=1, default='S')),
                ('course', models.ForeignKey(related_name='member', to='api.Course')),
                ('member', models.ForeignKey(related_name='course', to='api.Member')),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionFile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=api.models.SubmissionFile.generate_filename)),
                ('sha', models.CharField(max_length=1024)),
                ('submission', models.ForeignKey(related_name='files', to='api.AssignmentSubmission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubmissionReview',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('points', models.PositiveSmallIntegerField(default=0)),
                ('author', models.ForeignKey(to='api.Member')),
                ('submission', models.ForeignKey(related_name='reviews', to='api.AssignmentSubmission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='courseannouncement',
            name='author',
            field=models.ForeignKey(to='api.Member'),
        ),
        migrations.AddField(
            model_name='courseannouncement',
            name='course',
            field=models.ForeignKey(related_name='announcements', to='api.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='members',
            field=models.ManyToManyField(related_name='courses', to='api.Member', through='api.Membership'),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='assignment',
            field=models.ForeignKey(to='api.CourseAssignment'),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='author',
            field=models.ForeignKey(to='api.Member'),
        ),
        migrations.AddField(
            model_name='announcementcomment',
            name='announcement',
            field=models.ForeignKey(related_name='comments', to='api.CourseAnnouncement'),
        ),
        migrations.AddField(
            model_name='announcementcomment',
            name='author',
            field=models.ForeignKey(to='api.Member'),
        ),
    ]
