from django.conf import settings
from django.core.mail import send_mail


TEAMPLATE_FORGOT = getattr(settings, 'EMAIL_FORGOT_PWD_TEMPLATE', None)


def send_forgot_pwd_email(user, password):
    msg = TEAMPLATE_FORGOT.format(username=user.username, password=password)

    send_mail('Нова парола за вход в Lifebelt', msg,
              'noreply@elsys-bg.org', recipient_list=[user.email], html_message=msg,
              fail_silently=False)
