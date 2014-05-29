#encoding: utf-8
"""
Django settings for revengeBook project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# Project dir carga hasta nombre-proyecto/nombre-proyecto (a la altura de
# url.py y settings.py)
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# base dir carga hasta nombre-proyecto/ (a la altura de manage.py
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
          ('Alberto', 'a.vara.1986@gmail.com'),
          )
MANAGERS = ADMINS
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^kg1xhv)b#+(9%!=gu8h0d=-#mh(f5@=wm^cbd^**0s!ruibf7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'revengeapp',
    'revengeusers',
    'milestones',
    'south',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.bitbucket',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'revengeBook.urls'

WSGI_APPLICATION = 'revengeBook.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'revengeBook', 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'revengeBook', 'media')

MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'revengeusers.User'

LOGIN_URL = '/'

# Additional locations of static files
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'milestones.context_processors.get_revenge_points',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)
#SOCIAL AUTH
ACCOUNT_EMAIL_REQUIRED = True

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
        {'SCOPE': ['email', 'publish_stream'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
        'LOCALE_FUNC': lambda request: 'es_ES',
        'VERIFIED_EMAIL': False
        },
     'google':
        { 'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile'],
          'AUTH_PARAMS': { 'access_type': 'online' }
        }
    }
#MAIL. YOU MUST ADD YOUR CONNECTION
#MAIL


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
