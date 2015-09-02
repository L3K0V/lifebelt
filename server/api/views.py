import csv
import json
import datetime
from io import StringIO

from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import viewsets
from rest_framework import response
from rest_framework import status

from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from api.serializers import MemberSerializer
from api.models import Member
from django.contrib.auth.models import User

from api.serializers import CourseSerializer
from api.models import Course

from api.serializers import MembershipSerializer
from api.models import Membership

from api.serializers import CourseAssignmentSerializer
from api.models import CourseAssignment

from api.serializers import AssignmentSubmissionSerializer
from api.models import AssignmentSubmission

from api.serializers import SubmissionFileSerializer
from api.models import SubmissionFile

from api.serializers import SubmissionReviewSerializer
from api.models import SubmissionReview

from api.serializers import CourseAnnouncementSerializer
from api.models import CourseAnnouncement

from api.serializers import AnnouncementCommentSerializer
from api.models import AnnouncementComment

from api.serializers import AuthCustomTokenSerializer

from api.email import send_enroll_email, send_forgot_pwd_email

SESSION_AGE = getattr(settings, 'LIFEBELT_AUTH_TOKEN_AGE', None)
CSV_FORMAT = getattr(settings, 'CVS_MEMBERS_IMPORT_FORMAT', None)


class CSRFProtectedModelViewSet(viewsets.ModelViewSet):
    @method_decorator(ensure_csrf_cookie)
    def create(self, request):
        return super(CSRFProtectedModelViewSet, self).create(request)

    @method_decorator(ensure_csrf_cookie)
    def update(self, request, **kwargs):
        return super(CSRFProtectedModelViewSet, self).update(request, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def partial_update(self, request, **kwargs):
        return super(CSRFProtectedModelViewSet, self).partial_update(request, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def destroy(self, request, **kwargs):
        return super(CSRFProtectedModelViewSet, self).destroy(request, **kwargs)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('-id')
    serializer_class = MemberSerializer


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


class MembershipViewSet(CSRFProtectedModelViewSet):
    queryset = Membership.objects.all().order_by('-id')
    serializer_class = MembershipSerializer

    def list(self, request, course_pk=None):
        queryset = Membership.objects.filter(course=course_pk)
        serializer = MembershipSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None):
        queryset = Membership.objects.filter(pk=pk, course=course_pk)
        membership = get_object_or_404(queryset, pk=pk)
        serializer = MembershipSerializer(membership, context={'request': request})
        return response.Response(serializer.data)


class CourseAssignmentViewSet(CSRFProtectedModelViewSet):
    queryset = CourseAssignment.objects.all().order_by('-id')
    serializer_class = CourseAssignmentSerializer

    @method_decorator(ensure_csrf_cookie)
    def create(self, request, course_pk=None):
        context = {'request': request, 'course_pk': course_pk}
        serializer = CourseAssignmentSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, course_pk=None):
        queryset = CourseAssignment.objects.filter(course=course_pk)
        serializer = CourseAssignmentSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None):
        queryset = CourseAssignment.objects.filter(pk=pk, course=course_pk)
        assignment = get_object_or_404(queryset, pk=pk)
        serializer = CourseAssignmentSerializer(assignment, context={'request': request})
        return response.Response(serializer.data)


class AssignmentSubmissionViewSet(CSRFProtectedModelViewSet):
    serializer_class = AssignmentSubmissionSerializer
    queryset = AssignmentSubmission.objects.all().order_by('-id')

    def list(self, request, course_pk=None, assignment_pk=None):
        queryset = AssignmentSubmission.objects.filter(assignment__course=course_pk, assignment=assignment_pk)
        serializer = AssignmentSubmissionSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None, assignment_pk=None):
        queryset = AssignmentSubmission.objects.filter(pk=pk, assignment__course=course_pk, assignment=assignment_pk)
        submission = get_object_or_404(queryset, pk=pk)
        serializer = AssignmentSubmissionSerializer(submission, context={'request': request})
        return response.Response(serializer.data)

    @method_decorator(ensure_csrf_cookie)
    def create(self, request, course_pk=None, assignment_pk=None):
        context = {'request': request, 'course_pk': course_pk, 'assignment_pk': assignment_pk}
        serializer = AssignmentSubmissionSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SubmissionReviewViewSet(CSRFProtectedModelViewSet):
    serializer_class = SubmissionReviewSerializer
    queryset = SubmissionReview.objects.all().order_by('-id')

    def list(self, request, pk=None, course_pk=None, assignment_pk=None, submission_pk=None):
        queryset = SubmissionReview.objects.filter(submission=submission_pk)
        serializer = SubmissionReviewSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None, assignment_pk=None, submission_pk=None):
        queryset = SubmissionReview.objects.filter(pk=pk, submission=submission_pk)
        submission = get_object_or_404(queryset, pk=pk)
        serializer = SubmissionReviewSerializer(submission)
        return response.Response(serializer.data)

    @method_decorator(ensure_csrf_cookie)
    def create(self, request, pk=None, course_pk=None, assignment_pk=None, submission_pk=None):
        context = {'request': request, 'course_pk': course_pk, 'assignment_pk': assignment_pk, 'submission_pk': submission_pk}
        serializer = SubmissionReviewSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SubmissionFileUploadViewSet(CSRFProtectedModelViewSet):
    serializer_class = SubmissionFileSerializer
    queryset = SubmissionFile.objects.all().order_by('-id')
    parser_classes = (MultiPartParser, FormParser,)

    def list(self, request, pk=None, course_pk=None, assignment_pk=None, submission_pk=None):
        queryset = SubmissionFile.objects.filter(submission=submission_pk)
        serializer = SubmissionFileSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None, assignment_pk=None, submission_pk=None):
        queryset = SubmissionFile.objects.filter(pk=pk, submission=submission_pk)
        submission = get_object_or_404(queryset, pk=pk)
        serializer = SubmissionFileSerializer(submission)
        return response.Response(serializer.data)

    @method_decorator(ensure_csrf_cookie)
    def create(self, request, pk=None, course_pk=None, assignment_pk=None, submission_pk=None):
        context = {'request': request, 'course_pk': course_pk, 'assignment_pk': assignment_pk, 'submission_pk': submission_pk}
        serializer = SubmissionFileSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CourseAnnouncementViewSet(CSRFProtectedModelViewSet):
    serializer_class = CourseAnnouncementSerializer
    queryset = CourseAnnouncement.objects.all().order_by('-id')

    def list(self, request, pk=None, course_pk=None):
        queryset = CourseAnnouncement.objects.filter(course=course_pk)
        serializer = CourseAnnouncementSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None):
        queryset = CourseAnnouncement.objects.filter(pk=pk, course=course_pk)
        announcement = get_object_or_404(queryset, pk=pk)
        serializer = CourseAnnouncementSerializer(announcement)
        return response.Response(serializer.data)

    @method_decorator(ensure_csrf_cookie)
    def create(self, request, pk=None, course_pk=None):
        context = {'request': request, 'course_pk': course_pk}
        serializer = CourseAnnouncementSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AnnouncementCommentViewSet(CSRFProtectedModelViewSet):
    serializer_class = AnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all().order_by('-id')

    def list(self, request, pk=None, course_pk=None, announcement_pk=None):
        queryset = AnnouncementComment.objects.filter(announcement=announcement_pk)
        serializer = AnnouncementCommentSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None, announcement_pk=None):
        queryset = AnnouncementComment.objects.filter(pk=pk, announcement=announcement_pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = AnnouncementCommentSerializer(comment)
        return response.Response(serializer.data)

    @method_decorator(ensure_csrf_cookie)
    def create(self, request, pk=None, course_pk=None, announcement_pk=None):
        context = {'request': request, 'course_pk': course_pk, 'announcement_pk': announcement_pk}
        serializer = AnnouncementCommentSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ObtainExpiringAuthToken(ObtainAuthToken):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = AuthCustomTokenSerializer(context={'request': request}, data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            utc_now = timezone.now()
            if not created and token.created < utc_now - SESSION_AGE:
                token.delete()
                token = Token.objects.create(user=user)
                token.created = timezone.now()
                token.save()

                login(request, user)

            request.session.set_test_cookie()
            response_data = {'token': token.key}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticatedMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Member.objects.all().order_by('-id')
    serializer_class = MemberSerializer

    @detail_route(methods=['get'])
    def authenticated(self, request, *args, **kwargs):
        queryset = Member.objects.filter(user=request.user)
        serializer = MemberSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)


class InvalidateAuthToken(APIView):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        if request.user.is_authenticated():
            token = Token.objects.get(user=request.user)

            if token:
                token.delete()

            logout(request)

            if request.session.test_cookie_worked():
                print(">>>> TEST COOKIE WORKED!")
                request.session.delete_test_cookie()
            return HttpResponse('', status=status.HTTP_204_NO_CONTENT)

        return HttpResponse('', status=status.HTTP_400_BAD_REQUEST)


class CourseMembersImportViewSet(viewsets.ViewSet):
    @method_decorator(ensure_csrf_cookie)
    def create(self, request, course_pk=None):

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
                member = Member.objects.create(user=user,
                                               github=row[CSV_FORMAT['github']],
                                               student_class=row[CSV_FORMAT['student_class']],
                                               student_grade=row[CSV_FORMAT['student_grade']],
                                               student_number=row[CSV_FORMAT['student_number']])
                membership = Membership.objects.create(member=member, course=course, role='S')

                send_enroll_email(course, user, password)

        return HttpResponse('', status=status.HTTP_204_NO_CONTENT)


class RenewMemberPassword(APIView):
    permission_classes = ()

    def post(self, request):
        email = request.data['email']

        user = User.objects.get(username=email)

        if user:
            password = User.objects.make_random_password()

            user.set_password(password)
            user.save()

            send_forgot_pwd_email(user, password)

            return HttpResponse('', status=status.HTTP_204_NO_CONTENT)
