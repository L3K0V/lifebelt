from rest_framework import viewsets

from lifebelt.apps.core.courses.models import Course, Assignment
from lifebelt.apps.core.courses.serializers import CourseSerializer, AssignmentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by('-id')
    serializer_class = AssignmentSerializer
