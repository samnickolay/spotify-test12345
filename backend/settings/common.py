"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import ssl  # don't remove!

# import re
import textwrap
import json
import urllib
import urllib.request
from dotenv import load_dotenv

from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from django.core.serializers.json import DjangoJSONEncoder


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DOTENV_FILE = os.path.join(BASE_DIR, "env.django")
if os.path.isfile(DOTENV_FILE):
    print('found env.django file')
    load_dotenv(DOTENV_FILE)
else:
    print('could not find env.django file!')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


ENVIRONMENT = os.getenv('ENVIRONMENT')


ALLOWED_HOSTS = ['*']

# Application definition
PREREQUISITE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    "rest_framework_api_key",
    'corsheaders',
]

PROJECT_APPS = [
    'users.apps.UsersConfig',
    'accounts',
]

INSTALLED_APPS = PREREQUISITE_APPS + PROJECT_APPS

# tells django to use custom User model instead of default
AUTH_USER_MODEL = 'users.CustomUser'

ANONYMOUS_USER_NAME = 'Anonymous'

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',  # new
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # new

    # 'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'corsheaders.middleware.CorsPostCsrfMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {}

#
# Database settings in [environment].py files.
#


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Pacific'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_jwt_permission.permissions.JWTAPIPermission',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = ['https://team-18.vizy.io']
# CORS_ORIGIN_REGEX_WHITELIST = [r"^https://\w+\.vizy\.io.*$"]
# REGEX_LIST = [r'^/api/user/findYourTeams/.*$', r'^/api/team/login_type/.*$']
# CORS_URLS_REGEX = re.compile('|'.join(REGEX_LIST))

# AUTHENTICATION BACKENDS
#

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
    # 'guardian.backends.ObjectPermissionBackend',
]


#
# django_heroku settings in [environment].py files.
#


# ssl._create_default_https_context = ssl._create_unverified_context

# JWT_AUTH
# #

# JSON_URL = urllib.request.urlopen(AUTH0_DOMAIN + ".well-known/jwks.json")
# JWKS = json.loads(JSON_URL.read())
# CERT = '-----BEGIN CERTIFICATE-----\n' + textwrap.fill(JWKS['keys'][0]['x5c'][0], 64) + '\n-----END CERTIFICATE-----'

# CERTIFICATE = load_pem_x509_certificate(str.encode(CERT), default_backend())
# PUBLIC_KEY = CERTIFICATE.public_key()

# JWT_AUTH = {
#     'JWT_PAYLOAD_GET_USERNAME_HANDLER':
#         'backend.utils.jwt_get_username_from_payload_handler',
#     'JWT_DECODE_HANDLER':
#         'backend.utils.jwt_decode_token',
#     'JWT_ALGORITHM': 'RS256',
#     'JWT_AUDIENCE': AUTH0_API_IDENTIFIER,
#     'JWT_ISSUER': AUTH0_DOMAIN,
#     'JWT_AUTH_HEADER_PREFIX': 'Bearer',
# }
