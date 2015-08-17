from rest_framework import viewsets

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
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer


class MembershipViewSet(viewsets.ModelViewSet):

    queryset = Membership.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'create':
            return MembershipCreateSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return MembershipSerializer

        return MembershipCreateSerializer
