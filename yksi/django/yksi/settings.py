"""
Django settings for yksi project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json
import environ
import dj_database_url

env = environ.Env(DEBUG=(bool, False),)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third pary apps
    'crispy_forms',
    'storages',
    'django_cleanup',
    'djcelery_email',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'captcha',
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.github',
    # my apps
    'newsletter',
    'candidate',
    'myprofile',
)

SITE_ID = 1

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

# Authentication backends Setting
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'yksi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'yksi.wsgi.application'

# django-environ does not work with Pivotal Web Services and MySQL
# DATABASES = {
#     'default': env.db(), # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
# }
DATABASES = {'default': dj_database_url.config()}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# add S3 compatible storge
STATICFILES_STORAGE = 'yksi.custom_storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'yksi.custom_storages.MediaStorage'

# load user provided services
userservices = json.loads(os.environ['VCAP_SERVICES'])['user-provided']
for configs in userservices:
    if "ecs" in configs['name']:
        AWS_S3_HOST = configs['credentials']['HOST']
        AWS_ACCESS_KEY_ID = configs['credentials']['ACCESS_KEY_ID']
        AWS_SECRET_ACCESS_KEY = configs['credentials']['SECRET_ACCESS_KEY']
        S3_PUBLIC_URL = configs['credentials']['PUBLIC_URL']
    elif "mail" in configs['name']:
        EMAIL_HOST = configs['credentials']['HOST']
        EMAIL_HOST_USER = configs['credentials']['USER']
        EMAIL_HOST_PASSWORD = configs['credentials']['PASSWORD']
        EMAIL_PORT = int(configs['credentials']['PORT'])
        if configs['credentials']['TLS'] == 'True':
            EMAIL_USE_TLS = True
        else:
            EMAIL_USE_TLS = False

AWS_AUTO_CREATE_BUCKET = True
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False

STATIC_BUCKET_NAME = 'static'
STATIC_CUSTOM_DOMAIN = '%s.%s' %(STATIC_BUCKET_NAME,S3_PUBLIC_URL)
STATIC_URL = "http://%s/" % STATIC_CUSTOM_DOMAIN

MEDIA_BUCKET_NAME = 'media'
MEDIA_CUSTOM_DOMAIN = '%s.%s' %(MEDIA_BUCKET_NAME,S3_PUBLIC_URL)
MEDIA_URL = "http://%s/" % MEDIA_CUSTOM_DOMAIN

SECURE_BUCKET_NAME = 'secure'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_custom'),
)

# crispy
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG

# REST
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGE_SIZE': 10
}

#captcha
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'

# allauth
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_FORM_CLASS = 'myprofile.forms.SignupForm'
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_USERNAME_REQUIRED = True
#SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_PROVIDERS = \
    { 'github':
        {   'SCOPE': ['user:email'],
            'VERIFIED_EMAIL': True,
        },
    'facebook':
       {#'METHOD': 'js_sdk',
        'SCOPE': ['email', 'public_profile'],
        'VERIFIED_EMAIL': True,
        }
    }
LOGIN_REDIRECT_URL = '/'

# Celery settings
cloudamqp = json.loads(os.environ['VCAP_SERVICES'])['cloudamqp']
for creds in cloudamqp:
    if "rabbitmq" in creds['name']:
        BROKER_URL = creds['credentials']['uri']

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# https://www.cloudamqp.com/docs/celery.html
BROKER_POOL_LIMIT = 1 # Will decrease connection usage
BROKER_HEARTBEAT = 30 # Will detect stale connections faster
BROKER_CONNECTION_TIMEOUT = 30 # May require a long timeout due to Linux DNS timeouts etc
CELERY_RESULT_BACKEND = None
CELERY_SEND_EVENTS = False # Will not create celeryev.* queues
CELERY_EVENT_QUEUE_EXPIRES = 60 # Will delete all celeryev. queues without consumers after 1 minute.

# djcelery_email
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
