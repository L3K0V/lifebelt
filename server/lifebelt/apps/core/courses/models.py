from django.db import models

from lifebelt.apps.core.users.models import Member


class Course(models.Model):
    initials = models.CharField(max_length=16)
    full_name = models.CharField(max_length=48)
    description = models.TextField()
    year = models.PositiveSmallIntegerField()

    members = models.ManyToManyField(Member, through='Membership')

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Membership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.CharField(max_length=16)


class Assignment(models.Model):
    name = models.CharField(max_length=48)
    description = models.TextField()
    assignemnt_type = models.CharField(max_length=16)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()
    target = models.CharField(max_length=16)

    course = models.ForeignKey(Course)
