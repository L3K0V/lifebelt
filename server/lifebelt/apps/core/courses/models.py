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


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment)
    author = models.ForeignKey(Member)

    submitted_on = models.DateTimeField(auto_now_add=True)
    pull_request = models.PositiveSmallIntegerField()
    grade = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=256)


class SubmissionFile(models.Model):
    submission = models.ForeignKey(AssignmentSubmission)

    file = models.FileField()
    sha = models.CharField(max_length=1024)


class SubmissionReview(models.Model):
    submission = models.ForeignKey(AssignmentSubmission)
    author = models.ForeignKey(Member)

    description = models.TextField()
    points = models.PositiveSmallIntegerField()
    reviewed_on = models.DateTimeField(auto_now_add=True)
