"""
Django settings for astrochallenge project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't_ncv-#2$+0h&u@w-!1qu*b(qa4459cli#49@t0nxq!5h6^4#p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'astrochallenge.accounts',
    'astrochallenge.objects',
    'astrochallenge.challenges',
    'registration',
    'bootstrap3',
    'django_gravatar',
    'timezone_field',
    'django_comments',
    'astro_comments',
    'endless_pagination',
    'easy_thumbnails',
    'django_markdown',
    'bootstrap3_datetime',
)

COMMENTS_APP = 'astro_comments'
SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'astrochallenge.accounts.middleware.TimezoneMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'astrochallenge.urls'

WSGI_APPLICATION = 'astrochallenge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = ''
MAILGUN_SERVER_NAME = 'astrochallenge.com'
DEFAULT_FROM_EMAIL = 'noreply@astrochallenge.com'

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'

TEMPLATE_DIRS = (
    os.path.join(APP_ROOT, 'templates'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

STATICFILES_DIRS = (
    os.path.join(APP_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

MEDIA_URL = '/media/'

BOOTSTRAP3 = {
    'css_url': '/static/css/bootstrap.min.css',
    'javascript_url': '/static/js/vendor/bootstrap.min.js',
}

THUMBNAIL_ALIASES = {
    '': {
        'tiny': {'size': (100, 100), 'crop': False},
        'detail': {'size': (500, 500), 'crop': False},
        'satellite': {'size': (175, 175), 'crop': False},
        'log': {'size': (200, 200), 'crop': False},
        'challenge': {'size': (350, 350), 'crop': 'smart'},
    }
}

THUMBNAIL_BASEDIR = 'thumbs'

# Astro Specific stuff

CATALOGS = {
    'M': 'Messier',
    'NGC': 'NGC',
    'C': 'Caldwell',
}

SOLAR_SYSTEM_OBJECT_TYPES = (
    ('P', 'planet'),
    ('DP', 'dwarf planet'),
    ('M', 'moon'),
    ('A', 'asteroid'),
    ('C', 'comet'),
    ('S', 'satellite'),
    ('SC', 'spacecraft'),
    ('ST', 'star'),
)

QUALITATIVE_RATINGS = (
    ('P', 'poor'),
    ('BA', 'below average'),
    ('A', 'average'),
    ('AA', 'above average'),
    ('E', 'excellent'),
)

CHALLENGE_TYPES = (
    ('astro object', 'astro object'),
    ('solar ststem object', 'solar system object'),
    ('composite', 'solar system or deep space object'),
)

try:
    from local_settings import *
except ImportError:
    pass

try:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS
except:
    pass
