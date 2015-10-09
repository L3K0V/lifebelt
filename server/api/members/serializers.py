import requests

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator

from api.courses.models import Course

from api.members.models import Member
from api.members.models import Membership

from github3 import GitHub

CLIENT_ID = getattr(settings, 'LIFEBELT_GITHUB_CLIENT_ID', None)
CLIENT_SECRET = getattr(settings, 'LIFEBELT_GITHUB_CLIENT_SECRET', None)


class MemberSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Member
        depth = 1
        fields = ('id', 'first_name', 'last_name', 'email', 'github', 'avatar_url', 'student_grade', 'student_class', 'student_number')

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


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('id', 'member', 'role')
        read_only_fields = ('id', 'course')

    def create(self, validated_data):
        course = Course.objects.get(pk=self.context.get('course_pk'))

        membership = Membership.objects.create(course=course, **validated_data)

        return membership


class AuthCustomTokenSerializer(serializers.Serializer):
    code = serializers.CharField()
    state = serializers.CharField()

    def validate(self, attrs):
        code = attrs.get('code')
        state = attrs.get('state')

        user = None

        if not CLIENT_ID or not CLIENT_SECRET:
            msg = 'Lifebelt not configurated properly. Please contact administrators'
            raise exceptions.ValidationError(msg)

        if code and state:
            headers = {'Accept': 'application/json'}
            data = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": code, "state": state}
            url = 'https://github.com/login/oauth/access_token'

            r = requests.post(url=url, headers=headers, data=data)

            if 'access_token' not in r.json():
                msg = 'This smells...'

                if 'error' in r.json():
                    msg = r.json()['error']

                raise exceptions.ValidationError(msg)

            token = r.json()['access_token']

            # https://github3py.readthedocs.org/en/master/
            gh = GitHub(token=token)

            print(gh.me().as_json())

            user = Member.objects.get(github_id=gh.me().id)

            if not user:
                msg = 'User with this GitHub name is not found'
                raise exceptions.ValidationError(msg)

            user.avatar_url = gh.me().as_dict().get('avatar_url')
            user.github_token = token
            user.save()
        else:
            msg = ('You must provide a valid email and a special code to authenticate')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user.user
        return attrs
