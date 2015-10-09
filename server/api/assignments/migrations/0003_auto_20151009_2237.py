# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course'),
        ('members', '0002_auto_20151009_2237'),
        ('assignments', '0002_assignmentsubmission_courseassignment_submissionfile_submissionreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissionreview',
            name='author',
            field=models.ForeignKey(to='members.Member'),
        ),
        migrations.AddField(
            model_name='submissionreview',
            name='submission',
            field=models.ForeignKey(to='assignments.AssignmentSubmission', related_name='reviews'),
        ),
        migrations.AddField(
            model_name='submissionfile',
            name='submission',
            field=models.ForeignKey(to='assignments.AssignmentSubmission', related_name='files'),
        ),
        migrations.AddField(
            model_name='courseassignment',
            name='course',
            field=models.ForeignKey(to='courses.Course', related_name='assignments'),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='assignment',
            field=models.ForeignKey(to='assignments.CourseAssignment', related_name='submissions'),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='author',
            field=models.ForeignKey(to='members.Member'),
        ),
        migrations.AlterUniqueTogether(
            name='assignmentsubmission',
            unique_together=set([('assignment', 'pull_request')]),
        ),
    ]
