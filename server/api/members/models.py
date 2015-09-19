from django.db import models
from django.contrib.auth.models import User

STUDENT = 'S'
TEACHER = 'T'

MEMBER_ROLE = (
    (STUDENT, 'Student'),
    (TEACHER, 'Teacher')
)

STUDENT_CLASSES = (
    ('A', 'A'),
    ('B', 'B'),
    ('V', 'V'),
    ('G', 'G')
)


class Member(models.Model):
    user = models.OneToOneField(User, related_name="member")
    github = models.CharField(max_length=48, blank=True)
    # github_id = models.BigIntegerField(blank=True)
    github_token = models.CharField(max_length=256, blank=True)
    avatar_url = models.CharField(max_length=256, blank=True)

    student_class = models.CharField(max_length=1, choices=STUDENT_CLASSES, blank=True, null=True)
    student_grade = models.PositiveSmallIntegerField(blank=True, null=True)
    student_number = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {} ({})'.format(self.user.first_name, self.user.last_name, self.user.email)


class Membership(models.Model):
    course = models.ForeignKey('courses.Course', related_name='member')
    member = models.ForeignKey('Member', related_name='course')
    role = models.CharField(max_length=1, choices=MEMBER_ROLE, default=STUDENT)
