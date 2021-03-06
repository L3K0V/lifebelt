from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

SESSION_AGE = getattr(settings, 'LIFEBELT_AUTH_TOKEN_AGE', None)


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        utc_now = timezone.now()

        if token.created < utc_now - SESSION_AGE:
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
