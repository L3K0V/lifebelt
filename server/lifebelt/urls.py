from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from api.views import MemberViewSet
from api.views import CourseViewSet
from api.views import MembershipViewSet
from api.views import CourseAssignmentViewSet
from api.views import AssignmentSubmissionViewSet
from api.views import SubmissionReviewViewSet
from api.views import SubmissionFileUploadViewSet
from api.views import CourseAnnouncementViewSet
from api.views import AnnouncementCommentViewSet

router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'courses', CourseViewSet, base_name='courses')

courses_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'memberships', MembershipViewSet, base_name='memberships')
courses_router.register(r'announcements', CourseAnnouncementViewSet, base_name='announcements')
courses_router.register(r'assignments', CourseAssignmentViewSet, base_name='assignments')

assignments_router = routers.NestedSimpleRouter(courses_router, r'assignments', lookup='assignment')
assignments_router.register(r'submissions', AssignmentSubmissionViewSet, base_name='submission')

announcements_router = routers.NestedSimpleRouter(courses_router, r'announcements', lookup='announcement')
announcements_router.register(r'comments', AnnouncementCommentViewSet, base_name='comments')

submission_router = routers.NestedSimpleRouter(assignments_router, r'submissions', lookup='submission')
submission_router.register(r'reviews', SubmissionReviewViewSet, base_name='review')
submission_router.register(r'files', SubmissionFileUploadViewSet, base_name='file')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(courses_router.urls)),
    url(r'^', include(announcements_router.urls)),
    url(r'^', include(assignments_router.urls)),
    url(r'^', include(submission_router.urls))
]

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
                            (r'files/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),)
