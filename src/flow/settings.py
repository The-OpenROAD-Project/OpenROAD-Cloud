# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import environ
from corsheaders.defaults import default_headers

# Deployment configurations
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('src')
ENV_PATH = str(APPS_DIR.path('.env'))
env = environ.Env()
if env.bool('READ_ENVFILE', default=True):
    env.read_env(ENV_PATH)


# URLs
BASE_URL = env.str("BASE_URL", default="localhost:8000")

# Login URL
LOGIN_URL='/login'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='r((ws^80$x*0sm6wdvqgi&l@eea^f@%!+9%ah35gcas6oukgj#')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', True)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=['localhost'])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'frontend',
    'runner_listener',
    'notifications'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR.path('notifications', 'templates')),
                 str(APPS_DIR.path('templates'))],
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

WSGI_APPLICATION = 'flow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASE_URL = 'sqlite:///db.sqlite3'
POSTGRES_HOST = env('POSTGRES_HOST', default=None)
POSTGRES_DB = env('POSTGRES_DB', default=None)
POSTGRES_USER = env('POSTGRES_USER', default=None)
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD', default=None)

if POSTGRES_HOST and POSTGRES_DB and POSTGRES_USER and POSTGRES_PASSWORD:
    DATABASE_URL = 'postgres://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@' + POSTGRES_HOST + '/' + POSTGRES_DB

DATABASES = {
    'default': env.db('DATABASE_URL', default=DATABASE_URL),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = 600

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# STATIC_ROOT = env.str("DJANGO_STATIC_ROOT", default=str(APPS_DIR.path('assets')))
STATIC_URL = env.str("DJANGO_STATIC_URL", default='/static/')
STATICFILES_DIRS = (os.path.join(str(APPS_DIR), "assets"), )


# Design path on the file system
DESIGNS_DIR = env.str("DESIGNS_DIR", default=str(APPS_DIR.path('designs')))
VALIDATION_TMP_DIR = env.str("VALIDATION_TMP_DIR", default=str(APPS_DIR.path('validation_tmp')))

# Email Configurations
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='OpenROAD Flow <flow@theopenroadproject.org>')
ADMIN_NAME = env.str('ADMIN_NAME', default='Abdelrahman')
ADMIN_EMAIL = env.str('ADMIN_EMAIL', default='abdelrahman_ibrahim@brown.edu')

EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=25)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)

# Session Settings
SESSION_COOKIE_AGE = 24 * 60 * 60    # 1 day in seconds


# Celery Stuff
BROKER_URL = env.str("BROKER_URL", default='redis://localhost:6379')
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default='redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/New_York'

# Runner Endpoints
RUNNER_URL=env.str("RUNNER_URL", default='localhost:8001')