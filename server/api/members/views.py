import json
from django.conf import settings
from django.utils import timezone

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from django.http import HttpResponse

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import response
from rest_framework import status

from rest_framework.decorators import detail_route
from rest_framework.views import APIView

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from api import CSRFProtectedModelViewSet

from api.members.serializers import MemberSerializer, MembershipSerializer
from api.members.models import Member, Membership

from api.members.serializers import AuthCustomTokenSerializer

from api.members.email import send_forgot_pwd_email

SESSION_AGE = getattr(settings, 'LIFEBELT_AUTH_TOKEN_AGE', None)


class MembershipViewSet(CSRFProtectedModelViewSet):
    queryset = Membership.objects.all().order_by('-id')
    serializer_class = MembershipSerializer

    @method_decorator(ensure_csrf_cookie)
    def create(self, request, course_pk=None):
        context = {'request': request, 'course_pk': course_pk}
        serializer = MembershipSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, course_pk=None):
        queryset = Membership.objects.filter(course=course_pk)
        serializer = MembershipSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, course_pk=None):
        queryset = Membership.objects.filter(pk=pk, course=course_pk)
        membership = get_object_or_404(queryset, pk=pk)
        serializer = MembershipSerializer(membership, context={'request': request})
        return response.Response(serializer.data)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('-id')
    serializer_class = MemberSerializer


class AuthenticatedMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Member.objects.all().order_by('-id')
    serializer_class = MemberSerializer

    @detail_route(methods=['get'])
    def authenticated(self, request, *args, **kwargs):
        queryset = Member.objects.get(user=request.user)
        serializer = MemberSerializer(queryset, many=False, context={'request': request})
        return response.Response(serializer.data)


class ObtainExpiringAuthToken(ObtainAuthToken):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = AuthCustomTokenSerializer(context={'request': request}, data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            utc_now = timezone.now()
            if not created and token.created < utc_now - SESSION_AGE:
                token.delete()
                token = Token.objects.create(user=user)
                token.created = timezone.now()
                token.save()

                login(request, user)

            request.session.set_test_cookie()
            response_data = {'token': token.key}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvalidateAuthToken(APIView):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        if request.user.is_authenticated():
            token = Token.objects.get(user=request.user)

            if token:
                token.delete()

            logout(request)

            if request.session.test_cookie_worked():
                print(">>>> TEST COOKIE WORKED!")
                request.session.delete_test_cookie()
            return HttpResponse('', status=status.HTTP_204_NO_CONTENT)

        return HttpResponse('', status=status.HTTP_400_BAD_REQUEST)


class RenewMemberPassword(APIView):
    permission_classes = ()

    def post(self, request):
        email = request.data['email']

        user = User.objects.get(username=email)

        if user:
            password = User.objects.make_random_password()

            user.set_password(password)
            user.save()

            send_forgot_pwd_email(user, password)

            return HttpResponse('', status=status.HTTP_204_NO_CONTENT)
