from django.contrib import admin
from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.routers import DefaultRouter

from rest_framework_nested import routers

from api.members.views import MemberViewSet
from api.courses.views import CourseViewSet
from api.members.views import MembershipViewSet
from api.assignments.views import CourseAssignmentViewSet
from api.assignments.views import AssignmentSubmissionViewSet
from api.assignments.views import SubmissionReviewViewSet
from api.assignments.views import SubmissionFileUploadViewSet
from api.announcements.views import CourseAnnouncementViewSet
from api.announcements.views import AnnouncementCommentViewSet
from api.members.views import ObtainExpiringAuthToken
from api.members.views import InvalidateAuthToken
from api.members.views import RenewMemberPassword
from api.courses.views import CourseMembersImportViewSet
from api.members.views import AuthenticatedMemberViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'members', MemberViewSet)
router.register(r'courses', CourseViewSet, base_name='courses')

courses_router = routers.NestedSimpleRouter(router, r'courses', lookup='course', trailing_slash=False)
courses_router.register(r'memberships', MembershipViewSet, base_name='memberships')
courses_router.register(r'announcements', CourseAnnouncementViewSet, base_name='announcements')
courses_router.register(r'assignments', CourseAssignmentViewSet, base_name='assignments')
courses_router.register(r'import', CourseMembersImportViewSet, base_name='import')

assignments_router = routers.NestedSimpleRouter(courses_router, r'assignments', lookup='assignment', trailing_slash=False)
assignments_router.register(r'submissions', AssignmentSubmissionViewSet, base_name='submission')

announcements_router = routers.NestedSimpleRouter(courses_router, r'announcements', lookup='announcement', trailing_slash=False)
announcements_router.register(r'comments', AnnouncementCommentViewSet, base_name='comments')

submission_router = routers.NestedSimpleRouter(assignments_router, r'submissions', lookup='submission', trailing_slash=False)
submission_router.register(r'reviews', SubmissionReviewViewSet, base_name='review')
submission_router.register(r'files', SubmissionFileUploadViewSet, base_name='file')

urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/', include(courses_router.urls, namespace='api')),
    url(r'^api/', include(announcements_router.urls, namespace='api')),
    url(r'^api/', include(assignments_router.urls, namespace='api')),
    url(r'^api/', include(submission_router.urls, namespace='api')),
    url(r'^api/auth/login$', ObtainExpiringAuthToken.as_view()),
    url(r'^api/auth/logout$', InvalidateAuthToken.as_view()),
    url(r'^api/auth/reset-password$', RenewMemberPassword.as_view()),
    url(r'^api/auth/me$', AuthenticatedMemberViewSet.as_view({'get': 'authenticated'}), name='authenticated')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), ]
    urlpatterns += [url(r'^admin/', include(admin.site.urls)), ]
