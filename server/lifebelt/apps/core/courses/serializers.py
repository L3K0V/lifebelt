from rest_framework import serializers

from lifebelt.apps.core.courses.models import Course, Membership, Assignment, AssignmentSubmission, SubmissionFile
from lifebelt.apps.core.users.serializers import MemberSerializer


class MembershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        member = MemberSerializer
        model = Membership
        fields = ('member', 'role')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=False,
        queryset=Membership.objects.all().order_by('-id'),
        view_name='membership-detail'
    )

    assignments = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=False,
        queryset=Assignment.objects.all().order_by('-id'),
        view_name='assignments-detail'
    )

    class Meta:
        model = Course
        fields = ('id', 'initials', 'full_name', 'description', 'year', 'members', 'assignments', 'created_date', 'modified_date')


class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id', 'name', 'description', 'assignemnt_type', 'start', 'end', 'target')


class AssignmentSubmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = ('author', 'submitted_on', 'pull_request', 'grade', 'description')


class SubmissionFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ('file', 'sha')
