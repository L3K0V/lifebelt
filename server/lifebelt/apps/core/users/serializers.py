from rest_framework import serializers

from django.contrib.auth.models import User

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

    def update(self, instance, validated_data):
        # user = User.objects.get(pk = instance.user.pk);
        user = instance.user
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
        user = User.objects.create(**user_data)

        member = Member.objects.create(user=user, **validated_data)
        return member
