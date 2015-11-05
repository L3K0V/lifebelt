from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework import response
from rest_framework import status

from rest_framework.views import APIView

from rest_framework.parsers import FormParser, MultiPartParser

from api import CSRFProtectedModelViewSet

from api.members.models import Member

from api.assignments.serializers import CourseAssignmentSerializer
from api.assignments.models import CourseAssignment

from api.assignments.serializers import AssignmentSubmissionSerializer
from api.assignments.models import AssignmentSubmission

from api.assignments.serializers import SubmissionFileSerializer
from api.assignments.models import SubmissionFile

from api.assignments.serializers import SubmissionReviewSerializer
from api.assignments.models import SubmissionReview

from api.assignments.serializers import AssignmentTestCaseSerializer
from api.assignments.models import AssignmentTestCase

from api.assignments.tasks import review_submission


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


class AssignmentTestCaseViewSet(CSRFProtectedModelViewSet):
    serializer_class = AssignmentTestCaseSerializer
    queryset = AssignmentTestCase.objects.all().order_by('-id')

    def list(self, request, course_pk=None, assignment_pk=None):
        queryset = AssignmentTestCase.objects.filter(assignment=assignment_pk)
        serializer = AssignmentTestCaseSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None, assignment_pk=None):
        queryset = AssignmentTestCase.objects.filter(pk=pk, assignment=assignment_pk)
        submission = get_object_or_404(queryset, pk=pk)
        serializer = AssignmentTestCaseSerializer(submission, context={'request': request})
        return response.Response(serializer.data)

    @method_decorator(ensure_csrf_cookie)
    def create(self, request, course_pk=None, assignment_pk=None):
        context = {'request': request, 'course_pk': course_pk, 'assignment_pk': assignment_pk}
        serializer = AssignmentTestCaseSerializer(context=context, data=request.data)
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


class AssignmentGitHubReceiveHook(APIView):

    # DjangoModelPermissions require this
    queryset = CourseAssignment.objects.none()
    permission_classes = []

    @method_decorator(csrf_exempt)
    def post(self, request):
        if ('pull_request' in request.data and 'action' in request.data and 'number' in request.data):
            if (request.data['action'] == 'opened' or request.data['action'] == 'reopened'):
                    member = Member.objects.get(github_id=request.data['pull_request']['user']['id'])

                    assignment = CourseAssignment.objects.get(code__in=request.data['pull_request']['body'].split())

                    if assignment:
                        new_submission = AssignmentSubmission.objects.create(
                            assignment=assignment,
                            author=member,
                            pull_request=request.data['pull_request']['html_url'],
                            grade=0,
                            description=request.data['pull_request']['body'])

                        if new_submission:
                            review_submission.delay(submission_pk=new_submission.pk)
                            return HttpResponse('Submission created!', status=status.HTTP_200_OK)
                        else:
                            return HttpResponse('Submission cannot be created', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return HttpResponse('Received but submission not created', status=status.HTTP_200_OK)
