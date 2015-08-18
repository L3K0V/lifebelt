from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import response

from api.serializers import MemberSerializer
from api.models import Member

from api.serializers import CourseSerializer
from api.models import Course

from api.serializers import MembershipSerializer, MembershipCreateSerializer
from api.models import Membership


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
