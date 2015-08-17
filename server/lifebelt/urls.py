from django.conf.urls import include, url

from rest_framework import routers

from api.views import MemberViewSet
from api.views import CourseViewSet
from api.views import MembershipViewSet


router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'memberships', MembershipViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
