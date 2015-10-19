from __future__ import absolute_import

from django.conf import settings

from celery import shared_task

from api.assignments.models import AssignmentSubmission
from api.assignments.models import SubmissionReview
from api.members.models import Member

from github3 import login

LIFEBELT_BOT = getattr(settings, 'LIFEBELT_BOT_TOKEN', None)


@shared_task
def review_submission(submission_pk):
    gh = login(token=LIFEBELT_BOT)

    submission = AssignmentSubmission.objects.get(pk=submission_pk)

    author = Member.objects.get(github_id=gh.me().id)

    if author:
        desc = 'Compiled and running without problems!'

        review = SubmissionReview.objects.create(
            author=author, submission=submission, points=1, description=desc)

        pr = gh.pull_request(submission.pull_request.split('/')[-1])
        pr.create_comment(desc)
