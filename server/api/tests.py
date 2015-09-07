from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory, APIClient

from rest_framework import status
from rest_framework.test import APITestCase

from api.views import AuthenticatedMemberViewSet
from api.views import CourseViewSet

from api.models import Course


class AuthenticationTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AuthenticatedMemberViewSet.as_view({'get': 'authenticated'})
        self.user = AnonymousUser()

    def test_annonymous_has_no_me(self):
        request = self.factory.get('api/auth/me')
        request.user = self.user

        response = self.view(request)
        self.assertEqual(response.status_code, 401)


class CoursesText(APITestCase):

    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = User.objects.create(username='lekov', first_name='asen', last_name='lekov', email='asenlekoff@gmail.com')
        self.user.set_password('lekov')

    def test_annonymous_cannot_create_course(self):
        """
        Ensure we can CANNOT create a new account object with annonymous user.
        """
        url = reverse('api:courses-list')
        data = {'initials': 'PO', 'full_name': 'Operation Systems', 'year': 2016}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_course(self):
        self.client.login(username='lekov', password='lekov')

        url = reverse('api:courses-list')
        data = {'initials': 'PO', 'full_name': 'Operation Systems', 'year': 2016}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
