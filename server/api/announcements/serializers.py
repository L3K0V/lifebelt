from rest_framework import serializers, exceptions

from api.members.models import Member
from api.courses.models import Course

from api.announcements.models import CourseAnnouncement
from api.announcements.models import AnnouncementComment


class AnnouncementCommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comment = serializers.CharField()

    class Meta:
        model = CourseAnnouncement
        fields = ('id', 'author', 'comment', 'date_created', 'date_modified')

    def create(self, validated_data):
        announcement = CourseAnnouncement.objects.get(pk=self.context.get('announcement_pk'))
        author = Member.objects.get(user=self.context.get('request').user)

        comment = AnnouncementComment.objects.create(author=author, announcement=announcement, **validated_data)

        return comment


class CourseAnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = AnnouncementCommentSerializer(many=True, read_only=True)

    class Meta:
        model = CourseAnnouncement
        fields = ('id', 'author', 'announcement', 'comments', 'date_created', 'date_modified')

    def create(self, validated_data):
        course = Course.objects.get(pk=self.context.get('course_pk'))
        author = Member.objects.get(user=self.context.get('request').user)

        announcement = CourseAnnouncement.objects.create(author=author, course=course, **validated_data)

        return announcement
