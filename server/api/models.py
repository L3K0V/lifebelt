from django.db import models
from django.contrib.auth.models import User

ADMIN = 'A'
STUDENT = 'S'
TEACHER = 'T'

MEMBER_ROLE = (
    (ADMIN, 'Admin'),
    (STUDENT, 'Student'),
    (TEACHER, 'Teacher')
)


class Member(models.Model):
    user = models.OneToOneField(User, related_name="member", on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=MEMBER_ROLE, default=STUDENT)
    github = models.CharField(max_length=48, blank=True)
    github_token = models.CharField(max_length=256, blank=True)
    avatar_url = models.CharField(max_length=256, blank=True)


class Course(models.Model):
    initials = models.CharField(max_length=16, blank=False)
    full_name = models.CharField(max_length=48, blank=False)
    description = models.TextField()
    year = models.PositiveSmallIntegerField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    members = models.ManyToManyField(Member, through='Membership', through_fields=('course', 'member'), related_name='courses')


class Membership(models.Model):
    course = models.ForeignKey(Course, related_name='member')
    member = models.ForeignKey(Member, related_name='course')
    role = models.CharField(max_length=1, choices=MEMBER_ROLE, default=STUDENT)


class CourseAssignment(models.Model):
    A = 'A'
    B = 'B'
    V = 'V'
    G = 'G'
    ALL = 'ALL'

    ASSIGNMENT_TARGET = (
        (A, 'A class'),
        (B, 'B class'),
        (V, 'V class'),
        (G, 'G class'),
        (ALL, 'ALL classes')
    )

    HOMEWORK = 'H'
    EXAM = 'E'
    PRACTICE = 'P'

    ASSIGNMENT_TYPE = (
        (HOMEWORK, 'Homework'),
        (EXAM, 'Exam'),
        (PRACTICE, 'Practice')
    )

    name = models.CharField(max_length=48)
    description = models.TextField()
    assignemnt_type = models.CharField(max_length=1, choices=ASSIGNMENT_TYPE, default=HOMEWORK)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()
    target = models.CharField(max_length=3, choices=ASSIGNMENT_TARGET, default=ALL)

    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(CourseAssignment)
    author = models.ForeignKey(Member)

    submitted_on = models.DateTimeField(auto_now_add=True)
    pull_request = models.PositiveSmallIntegerField()
    grade = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=256)


class SubmissionReview(models.Model):
    submission = models.ForeignKey(AssignmentSubmission)
    author = models.ForeignKey(Member)

    description = models.TextField()
    points = models.PositiveSmallIntegerField()
    reviewed_on = models.DateTimeField(auto_now_add=True)


class SubmissionFile(models.Model):
    submission = models.ForeignKey(AssignmentSubmission)

    file = models.FileField()
    sha = models.CharField(max_length=1024)


class ReviewComment():
    pass


class CourseAnnouncement():
    pass


class AnnouncementComment():
    pass
