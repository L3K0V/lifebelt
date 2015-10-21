from __future__ import absolute_import

from django.conf import settings

from celery import shared_task

from api.assignments.models import AssignmentSubmission
from api.assignments.models import SubmissionReview
from api.members.models import Member

from github3 import login

LIFEBELT_BOT = getattr(settings.local, 'LIFEBELT_BOT_TOKEN', None)


@shared_task
def review_submission(submission_pk):

    print(LIFEBELT_BOT)

    gh = login(token=LIFEBELT_BOT)

    print(gh.me())

    submission = AssignmentSubmission.objects.get(pk=submission_pk)

    print(submission.pull_request.split('/'))

    repo = gh.repository(submission.pull_request.split('/')[-4], submission.pull_request.split('/')[-3])

    author = Member.objects.get(github_id=gh.me().id)

    if True:
        desc = 'Compiled and running without problems!'

        review = SubmissionReview.objects.create(
            author=author, submission=submission, points=1, description=desc)

        course = submission.assignment.course
        course_dir = '{}/{}/{}'.format(getattr(settings, 'GIT_ROOT', None), course.year, course.initials)

        # TODO: actual git work! patch, compile, test

        repo = git.Repo(course_dir)
        o = repo.remotes.origin
        o.pull()

        repo.checkout('HEAD', b='review#{}'.format(submission.id))
        repo.git.am('-s', 'patch file.patch')

        # ... hw.py

        repo.git.checkout(D='review#{}'.format(submission.id))

        pr = repo.pull_request(submission.pull_request.split('/')[-1])
        pr.create_comment(desc)
