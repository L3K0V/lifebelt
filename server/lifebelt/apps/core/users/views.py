from rest_framework import viewsets

from lifebelt.apps.core.users.models import Member
from lifebelt.apps.core.users.serializers import MemberSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('-id')
    serializer_class = MemberSerializer
