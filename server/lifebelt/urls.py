"""lifebelt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework_nested import routers
from lifebelt.apps.core.courses.views import CourseViewSet, AssignmentViewSet,\
    AssignmentSubmissionViewSet, SubmissionFileViewSet
from lifebelt.apps.core.users.views import MemberViewSet

router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet, base_name='courses')
router.register(r'members', MemberViewSet, base_name='members')

courses_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'assignments', AssignmentViewSet)

assignments_router = routers.NestedSimpleRouter(courses_router, r'assignments', lookup='assignment')
assignments_router.register(r'submissions', AssignmentSubmissionViewSet, base_name='submissions')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^', include(courses_router.urls)),
    url(r'^', include(assignments_router.urls))
]
