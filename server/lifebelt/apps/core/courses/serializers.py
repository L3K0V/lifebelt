from rest_framework import serializers

from lifebelt.apps.core.courses.models import Course, Assignment


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('initials', 'full_name', 'description', 'year', 'created_date', 'modified_date')


class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assignment
        fields = ('name', 'description', 'assignemnt_type', 'start', 'end', 'target')
