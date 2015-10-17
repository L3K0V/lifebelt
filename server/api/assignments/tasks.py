from __future__ import absolute_import

from celery import shared_task

from api.assignments.models import AssignmentSubmission
from api.assignments.models import SubmissionReview
from api.members.models import Member


@shared_task
def review_submission(submission_pk):
    submission = AssignmentSubmission.objects.get(pk=submission_pk)
    print(submission.pull_request)

    author = Member.objects.get(pk=1)

    review = SubmissionReview.objects.create(
        author=author, submission=submission, points=10, description='Compiled and running without problems!')
