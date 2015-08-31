from django.conf import settings
from django.core.mail import send_mail

TEAMPLATE_ENROLL = getattr(settings, 'EMAIL_ENROLL_TEMPLATE', None)
TEAMPLATE_FORGOT = getattr(settings, 'EMAIL_FORGOT_PWD_TEMPLATE', None)


def send_enroll_email(course, user, password='error'):

    msg = TEAMPLATE_ENROLL.format(course=course.full_name, year=course.year, pwd=password, lifebelt='#', headquarters='#')

    send_mail('Записване за {} {}'.format(course.full_name, course.year), msg,
              'noreply@elsys-bg.org', recipient_list=[user.email], html_message=msg,
              fail_silently=False)


def send_forgot_pwd_email(user, password):
    msg = TEAMPLATE_FORGOT.format(username=user.username, password=password)

    send_mail('Нова парола за вход в Lifebelt', msg,
              'noreply@elsys-bg.org', recipient_list=[user.email], html_message=msg,
              fail_silently=False)
