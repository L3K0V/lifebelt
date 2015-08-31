from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

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


class DateModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Member(models.Model):
    user = models.OneToOneField(User, related_name="member")
    github = models.CharField(max_length=48, blank=True)
    github_token = models.CharField(max_length=256, blank=True)
    avatar_url = models.CharField(max_length=256, blank=True)

    student_class = models.CharField(max_length=1, choices=STUDENT_CLASSES, blank=True, null=True)
    student_grade = models.PositiveSmallIntegerField(blank=True, null=True)
    student_number = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {} ({})'.format(self.user.first_name, self.user.last_name, self.user.email)


class Course(DateModel):
    initials = models.CharField(max_length=16, blank=False)
    full_name = models.CharField(max_length=48, blank=False)
    description = models.TextField()
    year = models.PositiveSmallIntegerField()

    members = models.ManyToManyField(Member, through='Membership', through_fields=('course', 'member'), related_name='courses')

    def __str__(self):
        return '{} ({})'.format(self.full_name, self.year)


class Membership(models.Model):
    course = models.ForeignKey(Course, related_name='member')
    member = models.ForeignKey(Member, related_name='course')
    role = models.CharField(max_length=1, choices=MEMBER_ROLE, default=STUDENT)


class CourseAssignment(DateModel):
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
    assignment_type = models.CharField(max_length=1, choices=ASSIGNMENT_TYPE, default=HOMEWORK)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()
    target = models.CharField(max_length=3, choices=ASSIGNMENT_TARGET, default=ALL)

    course = models.ForeignKey(Course, related_name='assignments')

    def __str__(self):
        return self.name


class AssignmentSubmission(DateModel):
    assignment = models.ForeignKey(CourseAssignment)
    author = models.ForeignKey(Member)

    pull_request = models.PositiveSmallIntegerField(blank=True, null=True)
    grade = models.PositiveSmallIntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)


class SubmissionReview(DateModel):
    submission = models.ForeignKey(AssignmentSubmission, related_name='reviews')
    author = models.ForeignKey(Member)

    description = models.TextField()
    points = models.PositiveSmallIntegerField(default=0)


class SubmissionFile(DateModel):

    def generate_filename(self, filename):
        course_id = self.submission.assignment.course.id
        assignemnt_id = self.submission.assignment.id
        submission_id = self.submission.id
        return 'course/{}/assignemnt/{}/submission/{}/{}'.format(course_id, assignemnt_id, submission_id, filename)

    submission = models.ForeignKey(AssignmentSubmission, related_name='files')

    file = models.FileField(upload_to=generate_filename)
    sha = models.CharField(max_length=1024)


class CourseAnnouncement(DateModel):
    author = models.ForeignKey(Member)
    course = models.ForeignKey(Course, related_name='announcements')
    announcement = models.TextField()


class AnnouncementComment(DateModel):
    author = models.ForeignKey(Member)
    announcement = models.ForeignKey(CourseAnnouncement, related_name='comments')
    comment = models.CharField(max_length=256)
