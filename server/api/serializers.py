from django.contrib.auth.models import User

from rest_framework import serializers

from api.models import Member
from api.models import Course
from api.models import Membership
from api.models import CourseAssignment


class MemberSerializer(serializers.HyperlinkedModelSerializer):

    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    courses = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='courses-detail'
    )

    class Meta:
        model = Member
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'courses', 'github', 'github_token', 'avatar_url')
        lookup_field = 'github'

    def update(self, instance, validated_data):
        user = instance.user
        user.username = validated_data.get('user.email', user.email)
        user.email = validated_data.get('user.email', user.email)
        user.first_name = validated_data.get('user.first_name', user.first_name)
        user.last_name = validated_data.get('user.last_name', user.last_name)
        user.save()

        instance.role = validated_data.get('role', instance.role)
        instance.github = validated_data.get('github', instance.github)
        instance.github_token = validated_data.get('github_token', instance.github_token)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.save()

        return instance

    def create(self, validated_data):

        user_data = validated_data.pop('user')
        user_data['username'] = user_data.get('email')
        user = User.objects.create(**user_data)

        member = Member.objects.create(user=user, **validated_data)
        return member


class CourseSerializer(serializers.HyperlinkedModelSerializer):

    members = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='member-detail'
    )

    class Meta:
        model = Course
        fields = ('id', 'initials', 'full_name', 'description', 'year', 'members', 'date_created', 'date_modified')


class MembershipCreateSerializer(serializers.HyperlinkedModelSerializer):
    course_id = serializers.IntegerField()
    member_id = serializers.IntegerField()

    def create(self, validated_data):

        member = Member.objects.get(pk=validated_data.get('member_id'))
        course = Course.objects.get(pk=validated_data.get('course_id'))
        role = validated_data.get('role')

        membership = Membership.objects.create(member=member, course=course, role=role)

        return membership

    class Meta:
        model = Membership
        fields = ('id', 'course_id', 'member_id', 'role')


class MembershipSerializer(serializers.HyperlinkedModelSerializer):
    course = CourseSerializer()
    member = MemberSerializer()

    class Meta:
        model = Membership
        fields = ('id', 'course', 'member', 'role')


class CourseAssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseAssignment
        fields = ('id', 'name', 'description', 'assignment_type', 'start', 'end', 'target')

    def create(self, validated_data):
        course = Course.objects.get(pk=self.context.get('course_pk'))

        assignment = CourseAssignment.objects.create(course=course, **validated_data)

        return assignment
