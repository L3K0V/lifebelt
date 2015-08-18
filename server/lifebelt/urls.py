from django.conf.urls import include, url

from rest_framework_nested import routers

from api.views import MemberViewSet
from api.views import CourseViewSet
from api.views import MembershipViewSet
from api.views import CourseAssignmentViewSet
from api.views import AssignmentSubmissionViewSet
from api.views import SubmissionFileUploadViewSet


router = routers.SimpleRouter()
router.register(r'members', MemberViewSet)
router.register(r'courses', CourseViewSet, base_name='courses')

courses_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'memberships', MembershipViewSet, base_name='memberships')
courses_router.register(r'assignments', CourseAssignmentViewSet, base_name='assignments')

assignments_router = routers.NestedSimpleRouter(courses_router, r'assignments', lookup='assignment')
assignments_router.register(r'submissions', AssignmentSubmissionViewSet, base_name='submission')

submission_router = routers.NestedSimpleRouter(assignments_router, r'submissions', lookup='submission')
submission_router.register(r'upload', SubmissionFileUploadViewSet, base_name='upload')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(courses_router.urls)),
    url(r'^', include(assignments_router.urls)),
    url(r'^', include(submission_router.urls)),
]
