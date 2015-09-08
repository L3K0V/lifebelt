from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import viewsets
from rest_framework import response
from rest_framework import status

from api import CSRFProtectedModelViewSet

from api.announcements.serializers import CourseAnnouncementSerializer
from api.announcements.models import CourseAnnouncement

from api.announcements.serializers import AnnouncementCommentSerializer
from api.announcements.models import AnnouncementComment


class CourseAnnouncementViewSet(CSRFProtectedModelViewSet):
    serializer_class = CourseAnnouncementSerializer
    queryset = CourseAnnouncement.objects.all().order_by('-id')

    def list(self, request, pk=None, course_pk=None):
        queryset = CourseAnnouncement.objects.filter(course=course_pk)
        serializer = CourseAnnouncementSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None):
        queryset = CourseAnnouncement.objects.filter(pk=pk, course=course_pk)
        announcement = get_object_or_404(queryset, pk=pk)
        serializer = CourseAnnouncementSerializer(announcement)
        return response.Response(serializer.data)

    @method_decorator(ensure_csrf_cookie)
    def create(self, request, pk=None, course_pk=None):
        context = {'request': request, 'course_pk': course_pk}
        serializer = CourseAnnouncementSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AnnouncementCommentViewSet(CSRFProtectedModelViewSet):
    serializer_class = AnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all().order_by('-id')

    def list(self, request, pk=None, course_pk=None, announcement_pk=None):
        queryset = AnnouncementComment.objects.filter(announcement=announcement_pk)
        serializer = AnnouncementCommentSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None, announcement_pk=None):
        queryset = AnnouncementComment.objects.filter(pk=pk, announcement=announcement_pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = AnnouncementCommentSerializer(comment)
        return response.Response(serializer.data)

    @method_decorator(ensure_csrf_cookie)
    def create(self, request, pk=None, course_pk=None, announcement_pk=None):
        context = {'request': request, 'course_pk': course_pk, 'announcement_pk': announcement_pk}
        serializer = AnnouncementCommentSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
