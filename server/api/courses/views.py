import csv
from io import StringIO

from django.conf import settings

from django.http import HttpResponse

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import response
from rest_framework import status

from api import CSRFProtectedModelViewSet

from api.courses.serializers import CourseSerializer
from api.courses.models import Course

from api.courses.email import send_enroll_email

from api.members.models import Member, Membership

from github3 import GitHub

CSV_FORMAT = getattr(settings, 'CVS_MEMBERS_IMPORT_FORMAT', None)


class CourseViewSet(CSRFProtectedModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all().order_by('-id')

    def list(self, request,):
        queryset = Course.objects.filter()
        serializer = CourseSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Course.objects.filter()
        client = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(client, context={'request': request})
        return response.Response(serializer.data)


class CourseMembersImportViewSet(viewsets.ViewSet):
    @method_decorator(ensure_csrf_cookie)
    def create(self, request, course_pk=None):
        gh = GitHub()

        course = Course.objects.get(pk=course_pk)

        members = request.FILES['members']

        if members:
            csvf = StringIO(members.read().decode())
            reader = csv.DictReader(csvf, delimiter=',')
            for row in reader:
                password = User.objects.make_random_password()
                user = User.objects.create_user(first_name=row[CSV_FORMAT['first_name']],
                                                last_name=row[CSV_FORMAT['last_name']],
                                                email=row[CSV_FORMAT['email']],
                                                username=row[CSV_FORMAT['email']])
                user.set_password(password)
                user.save()

                github_user = gh.user(row[CSV_FORMAT['github']])

                member = Member.objects.create(user=user,
                                               github=row[CSV_FORMAT['github']],
                                               github_id=github_user.id,
                                               student_class=row[CSV_FORMAT['student_class']],
                                               student_grade=row[CSV_FORMAT['student_grade']],
                                               student_number=row[CSV_FORMAT['student_number']])
                membership = Membership.objects.create(member=member, course=course, role='S')

                send_enroll_email(course, user, password)

        return HttpResponse('', status=status.HTTP_204_NO_CONTENT)
