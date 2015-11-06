from __future__ import absolute_import

from django.conf import settings

from celery import shared_task

from api.assignments.models import AssignmentSubmission
from api.assignments.models import SubmissionReview
from api.members.models import Member

import tempfile

from git import Repo, GitCommandError
from github3 import login

LIFEBELT_BOT = getattr(settings, 'LIFEBELT_BOT_TOKEN', None)


@shared_task
def review_submission(submission_pk):

    gh = login(token=LIFEBELT_BOT)

    submission = AssignmentSubmission.objects.get(pk=submission_pk)
    pull_request_number = submission.pull_request.split('/')[-1]
    repo = gh.repository(submission.pull_request.split('/')[-4], submission.pull_request.split('/')[-3])
    author = Member.objects.get(github_id=gh.me().id)

    if author:
        desc = 'Compiled and running without problems!'

        review = SubmissionReview.objects.create(
            author=author, submission=submission, points=1, description=desc)

        course = submission.assignment.course
        course_dir = '{}/{}/{}'.format(getattr(settings, 'GIT_ROOT', None), course.year, course.initials)

        # TODO: actual git work! patch, compile, test

        r = Repo(course_dir)
        o = r.remotes.origin
        o.pull()

        pr = repo.pull_request(pull_request_number)

        with tempfile.NamedTemporaryFile() as temp:
            temp.write(pr.patch())
            temp.flush()
            print(temp)

            try:

                r.git.checkout('HEAD', b='review#{}'.format(submission.id))
                r.git.am(temp.name)
                r.git.branch(D='review#{}'.format(submission.id))

            except GitCommandError:
                pr.create_comment("Git error while preparing to review...")

        pr.create_comment(desc)
