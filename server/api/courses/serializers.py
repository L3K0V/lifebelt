from rest_framework import serializers, exceptions

from api.courses.models import Course
from api.members.serializers import MemberSerializer


class CourseSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        depth = 2
        fields = ('id', 'initials', 'full_name', 'description', 'year', 'repository', 'members', 'date_created', 'date_modified')
