from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import response
from rest_framework import status

from rest_framework.parsers import FormParser, MultiPartParser

from api.serializers import MemberSerializer
from api.models import Member

from api.serializers import CourseSerializer
from api.models import Course

from api.serializers import MembershipSerializer, MembershipCreateSerializer
from api.models import Membership

from api.serializers import CourseAssignmentSerializer
from api.models import CourseAssignment

from api.serializers import AssignmentSubmissionSerializer
from api.models import AssignmentSubmission

from api.serializers import SubmissionFileSerializer
from api.models import SubmissionFile


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('-id')
    serializer_class = MemberSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def list(self, request,):
        queryset = Course.objects.filter()
        serializer = CourseSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Course.objects.filter()
        client = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(client, context={'request': request})
        return response.Response(serializer.data)


class MembershipViewSet(viewsets.ModelViewSet):

    def list(self, request, course_pk=None):
        queryset = Membership.objects.filter(course=course_pk)
        serializer = MembershipSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None):
        queryset = Membership.objects.filter(pk=pk, course=course_pk)
        membership = get_object_or_404(queryset, pk=pk)
        serializer = MembershipSerializer(membership, context={'request': request})
        return response.Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'create':
            return MembershipCreateSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return MembershipSerializer

        return MembershipCreateSerializer


class CourseAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CourseAssignment.objects.all().order_by('-id')
    serializer_class = CourseAssignmentSerializer

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


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSubmissionSerializer

    def list(self, request, course_pk=None, assignment_pk=None):
        queryset = AssignmentSubmission.objects.filter(assignment__course=course_pk, assignment=assignment_pk)
        serializer = AssignmentSubmissionSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None, assignment_pk=None):
        queryset = AssignmentSubmission.objects.filter(pk=pk, assignment__course=course_pk, assignment=assignment_pk)
        submission = get_object_or_404(queryset, pk=pk)
        serializer = AssignmentSubmissionSerializer(submission)
        return response.Response(serializer.data)

    def create(self, request, course_pk=None, assignment_pk=None):
        context = {'request': request, 'course_pk': course_pk, 'assignment_pk': assignment_pk}
        serializer = AssignmentSubmissionSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SubmissionFileUploadViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionFileSerializer
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

    def create(self, request, pk=None, course_pk=None, assignment_pk=None, submission_pk=None):
        context = {'request': request, 'course_pk': course_pk, 'assignment_pk': assignment_pk, 'submission_pk': submission_pk}
        serializer = SubmissionFileSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
