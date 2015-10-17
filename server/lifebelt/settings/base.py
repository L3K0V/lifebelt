"""
Django settings for lifebelt project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import absolute_import
import os
import datetime
import djcelery

djcelery.setup_loader()

BROKER_URL = 'django://'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = '?5o;gAeZpe!u3ISOt7|)#Tx4GneshtodrugoJ2D8zI'

ALLOWED_HOSTS = []

LIFEBELT_AUTH_TOKEN_AGE = datetime.timedelta(days=7)

ANONYMOUS_USER_ID = 0

CVS_MEMBERS_IMPORT_FORMAT = {
    'first_name': 'Име',
    'last_name': 'Фамилия',
    'email': 'Имейл',
    'github': 'GitHub',
    'student_class': 'Паралелка',
    'student_grade': 'Клас',
    'student_number': 'Номер'
}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'kombu.transport.django',
    'rest_framework',
    'rest_framework.authtoken',
    'api.members',
    'api.courses',
    'api.assignments',
    'api.announcements',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'api.members.auth.ExpiringTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions',
    )
}

ROOT_URLCONF = 'lifebelt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lifebelt.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': '',        # Not used with sqlite3.
        'PASSWORD': '',    # Not used with sqlite3.
        'HOST': '',        # Set to empty string for localhost.
                           # Not used with sqlite3.
        'PORT': '',        # Set to empty string for default.
                           # Not used with sqlite3.
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
            'datefmt': '%y %b %d, %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'celery': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'celery.log',
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
        },
    },
    'loggers': {
        'celery': {
            'handlers': ['celery', 'console'],
            'level': 'DEBUG',
        },
    }
}

from logging.config import dictConfig
dictConfig(LOGGING)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'userfiles')
MEDIA_URL = '/files/'

STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, '../static'),
    os.path.join(BASE_DIR, '../../webapp/dist'),
)

EMAIL_ENROLL_TEMPLATE = """Здрасти,
<p>Ти беше записан <b>успешно</b> за курса по <a href="{lifebelt}">{course} ({year})</a> и затова ти изпращаме малко линкове и информация.</p>
<br>
<p>Преди всичко - това е твоята парола и не я казвай на никого: <strong>{pwd}</strong></p>
<br>
<p><a href="{headquarters}">Тук</a> можеш да видиш за това кога си присъствал и забележки, които сме писали за теб.</p>
<p> В <a href="http://lubo.elsys-bg.org/c-programming/">сайта на Любо</a> има обща информация за курса и всичко свързано с ТУЕС. </p>
<br>
<p>Няма нужда да отговаряш на това съобщение, то е генерирано автоматично...</p>
<br>
Поздрави!"""


EMAIL_FORGOT_PWD_TEMPLATE = """Здрасти,
<p>Ти поиска да ти бъде сменена паролата, затова ето ти нова: <strong>{password}</strong></p>
<p>Ако все пак си забравил кое ти е потребителското име: <strong>{username}</strong></p>
<br>
Поздрави!"""

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
