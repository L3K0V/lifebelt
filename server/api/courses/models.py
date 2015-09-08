from django.db import models


class Course(models.Model):
    initials = models.CharField(max_length=16, blank=False)
    full_name = models.CharField(max_length=48, blank=False)
    description = models.TextField()
    year = models.PositiveSmallIntegerField()

    members = models.ManyToManyField('members.Member', through='members.Membership', through_fields=('course', 'member'), related_name='courses')

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} ({})'.format(self.full_name, self.year)
