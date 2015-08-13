from rest_framework import viewsets

from lifebelt.apps.core.courses.models import Course, Assignment, Membership,\
    AssignmentSubmission, SubmissionFile
from lifebelt.apps.core.users.models import Member
from lifebelt.apps.core.courses.serializers import CourseSerializer, MembershipSerializer,\
    AssignmentSerializer, AssignmentSubmissionSerializer, SubmissionFileSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all().order_by('-id')
    serializer_class = MembershipSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by('-id')
    serializer_class = AssignmentSerializer


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all().order_by('-id')
    serializer_class = AssignmentSubmissionSerializer


class SubmissionFileViewSet(viewsets.ModelViewSet):
    queryset = SubmissionFile.objects.all().order_by('-id')
    serializer_class = SubmissionFileSerializer
