from django.db import models


class CourseAnnouncement(models.Model):
    author = models.ForeignKey('members.Member')
    course = models.ForeignKey('courses.Course', related_name='announcements')
    announcement = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class AnnouncementComment(models.Model):
    author = models.ForeignKey('members.Member')
    announcement = models.ForeignKey('CourseAnnouncement', related_name='comments')
    comment = models.CharField(max_length=256)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
