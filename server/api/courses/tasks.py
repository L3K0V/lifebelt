from __future__ import absolute_import

from django.conf import settings

from celery import shared_task

from api.courses.models import Course

from git import Repo

import os.path


@shared_task
def clone_course_repo(course_pk):
    course = Course.objects.get(pk=course_pk)
    course_dir = '{}/{}/{}'.format(getattr(settings, 'GIT_ROOT', None), course.year, course.initials)

    if not os.path.exists(course_dir) and course:
        print("Cloning...")
        Repo.clone_from(course.repository, course_dir)
