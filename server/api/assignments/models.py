import uuid
from django.db import models
from django.utils import timezone


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
    code = models.CharField(max_length=200, default=uuid.uuid4, editable=False)

    course = models.ForeignKey('courses.Course', related_name='assignments')

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey('CourseAssignment', related_name='submissions')
    author = models.ForeignKey('members.Member')

    pull_request = models.PositiveSmallIntegerField(blank=True, null=True)
    grade = models.PositiveSmallIntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('assignment', 'pull_request',)


class SubmissionReview(models.Model):
    submission = models.ForeignKey('AssignmentSubmission', related_name='reviews')
    author = models.ForeignKey('members.Member')

    description = models.TextField()
    points = models.PositiveSmallIntegerField(default=0)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class SubmissionFile(models.Model):

    def generate_filename(self, filename):
        course_id = self.submission.assignment.course.id
        assignemnt_id = self.submission.assignment.id
        submission_id = self.submission.id
        return 'course/{}/assignemnt/{}/submission/{}/{}'.format(course_id, assignemnt_id, submission_id, filename)

    submission = models.ForeignKey('AssignmentSubmission', related_name='files')

    file = models.FileField(upload_to=generate_filename)
    sha = models.CharField(max_length=1024)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
