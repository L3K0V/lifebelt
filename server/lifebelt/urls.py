from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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
from api.views import ObtainExpiringAuthToken
from api.views import InvalidateAuthToken
from api.views import RenewMemberPassword
from api.views import CourseMembersImportViewSet
from api.views import AuthenticatedMemberViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'members', MemberViewSet)
router.register(r'courses', CourseViewSet, base_name='courses')

courses_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'memberships', MembershipViewSet, base_name='memberships')
courses_router.register(r'announcements', CourseAnnouncementViewSet, base_name='announcements')
courses_router.register(r'assignments', CourseAssignmentViewSet, base_name='assignments')
courses_router.register(r'import', CourseMembersImportViewSet, base_name='import')

assignments_router = routers.NestedSimpleRouter(courses_router, r'assignments', lookup='assignment')
assignments_router.register(r'submissions', AssignmentSubmissionViewSet, base_name='submission')

announcements_router = routers.NestedSimpleRouter(courses_router, r'announcements', lookup='announcement')
announcements_router.register(r'comments', AnnouncementCommentViewSet, base_name='comments')

submission_router = routers.NestedSimpleRouter(assignments_router, r'submissions', lookup='submission')
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
