from rest_framework import serializers

from lifebelt.apps.core.users.models import Member


class MemberSerializer(serializers.HyperlinkedModelSerializer):

    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Member
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'role', 'github', 'github_token', 'avatar_url')
