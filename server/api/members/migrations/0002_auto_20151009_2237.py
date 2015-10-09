# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_course'),
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('github', models.CharField(max_length=48, blank=True)),
                ('github_id', models.PositiveIntegerField(blank=True, null=True)),
                ('github_token', models.CharField(max_length=256, blank=True)),
                ('avatar_url', models.CharField(max_length=256, blank=True)),
                ('student_class', models.CharField(max_length=1, blank=True, null=True, choices=[('A', 'A'), ('B', 'B'), ('V', 'V'), ('G', 'G')])),
                ('student_grade', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('student_number', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='member')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('role', models.CharField(max_length=1, default='S', choices=[('S', 'Student'), ('T', 'Teacher')])),
                ('course', models.ForeignKey(to='courses.Course', related_name='member')),
                ('member', models.ForeignKey(to='members.Member', related_name='course')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('course', 'member')]),
        ),
    ]
