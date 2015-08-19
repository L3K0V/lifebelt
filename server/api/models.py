from django.db import models
from django.utils import timezone
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
    user = models.OneToOneField(User, related_name="member")
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
    assignment_type = models.CharField(max_length=1, choices=ASSIGNMENT_TYPE, default=HOMEWORK)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()
    target = models.CharField(max_length=3, choices=ASSIGNMENT_TARGET, default=ALL)

    course = models.ForeignKey(Course, related_name='assignments')


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(CourseAssignment)
    author = models.ForeignKey(Member)

    submitted_on = models.DateTimeField(auto_now_add=True)
    pull_request = models.PositiveSmallIntegerField(blank=True, null=True)
    grade = models.PositiveSmallIntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)


class SubmissionReview(models.Model):
    submission = models.ForeignKey(AssignmentSubmission, related_name='reviews')
    author = models.ForeignKey(Member)

    description = models.TextField()
    points = models.PositiveSmallIntegerField(default=0)
    reviewed_on = models.DateTimeField(auto_now_add=True)


class SubmissionFile(models.Model):

    def generate_filename(self, filename):
        course_id = self.submission.assignment.course.id
        assignemnt_id = self.submission.assignment.id
        submission_id = self.submission.id
        return 'course/{}/assignemnt/{}/submission/{}/{}'.format(course_id, assignemnt_id, submission_id, filename)

    submission = models.ForeignKey(AssignmentSubmission, related_name='files')

    file = models.FileField(upload_to=generate_filename)
    sha = models.CharField(max_length=1024)
    uploaded_on = models.DateTimeField(auto_now_add=True)


class ReviewComment(models.Model):
    review = models.ForeignKey(SubmissionReview, related_name='comments')
    author = models.ForeignKey(Member)

    comment = models.TextField()
    commentted_on = models.DateTimeField(auto_now_add=True)


class CourseAnnouncement():
    pass


class AnnouncementComment():
    pass
