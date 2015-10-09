# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course'),
        ('members', '0002_auto_20151009_2237'),
        ('announcements', '0002_announcementcomment_courseannouncement'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseannouncement',
            name='author',
            field=models.ForeignKey(to='members.Member'),
        ),
        migrations.AddField(
            model_name='courseannouncement',
            name='course',
            field=models.ForeignKey(to='courses.Course', related_name='announcements'),
        ),
        migrations.AddField(
            model_name='announcementcomment',
            name='announcement',
            field=models.ForeignKey(to='announcements.CourseAnnouncement', related_name='comments'),
        ),
        migrations.AddField(
            model_name='announcementcomment',
            name='author',
            field=models.ForeignKey(to='members.Member'),
        ),
    ]
