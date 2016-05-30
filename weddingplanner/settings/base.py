"""
Base Django settings for weddingplanner project.

This file contains the base settings that are valid for all environments. The environment
specific settins files can then override these. (See environment.py)

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

from django.core.urlresolvers import reverse_lazy

# TODO: move this into a separate file, probably in libs
def _apply(fn,x,times,):
    if times > 1:
        return fn(_apply(fn,x,times-1))
    else:
        return fn(x)

PROJECT_ROOT = _apply(os.path.dirname, os.path.abspath(__file__), 3)

PROJECT_NAME = 'weddingplanner'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = r'23hvwf@cm4n6fa7rvbohkp4!taw4op9vo%xmhuoxp9qcr2(dze'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

# Recipients of traceback emails and other notifications.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Sample settings for Postgresql. The actual settings should live in the environment specific
    #  files.
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database_name',
        'USER': 'user_name',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION

########## CACHE CONFIGURATION
#CACHES = {
#    'default': {
#        'BACKEND': 'django_redis.cache.RedisCache',
#        'LOCATION': '127.0.0.1:6379:1',
#        'OPTIONS': {
#            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#            'SOCKET_TIMEOUT': 5,  # in seconds
#            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
#            # Native parser for added performance (can be included later, maybe for deployment only
#            # 'PARSER_CLASS': 'redis.connection.HiredisParser',
#            # 'PASSWORD': 'secretpassword',  # Optional
#        }
#    }
#}
########## END CACHE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
#    'blanc_basic_pages.context_processors.page',
    'settings_context_processor.context_processors.settings',
    # 'django.core.context_processors.csrf',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    os.path.join(PROJECT_ROOT, 'front-end', 'templates')
)
########## END TEMPLATE CONFIGURATION


########## APP CONFIGURATION

# Application definition
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    # 3rd party apps:
#    'easy_thumbnails',
#    'image_cropping', # -> report missing dependency (easy-thumbnails)

    # Maybe needed for deployment only?
#    'compressor',
    'django_forms_bootstrap',
#    'rest_framework',
    'jsonify',
    'raven.contrib.django.raven_compat',
    'settings_context_processor',

    # blanc-basic-pages
    #'mptt',
    #'django_mptt_admin',
    #'blanc_basic_pages',

    # django-reversion (for versioning objects, used for page content versioning)
#    'reversion',

    # django-reversion-compare (adds diff views to django-reversion)

    # 'reversion_compare',

    # Add local apps here: (note that only the last element is used as the 'app name'!)
    'weddingplanner.apps.main',

)
########## END APP CONFIGURATION

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'cached_auth.Middleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_NAME

APPEND_SLASH = True

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

########## STATIC FILE CONFIGURATION
# Static files get collected here upon deployment
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'assets')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# Static files get collected *from* these directories by the FileSystemFinder. (Other finders
#  may collect files from other locations as well.)
# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'compressor.finders.CompressorFinder',
)
########## END STATIC FILE CONFIGURATION

########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
########## END SITE CONFIGURATION

########## SECURITY CONFIGURATION
# Password hashers are in the order of strength. Think about removing the ones that you don't
#  want to use to prevent surprises.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Disable access to cookies by JavaScript (on most browsers...)
SESSION_COOKIE_HTTPONLY = True

# Set this to true if you are using https
SESSION_COOKIE_SECURE = False

########## END SECURITY CONFIGURATION

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

# TODO: add sample sentry config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(module)s[%(process)d] %(levelname)s -- %(message)s',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO'
        },
    }
}
########## END LOGGING CONFIGURATION

########## REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

########## END REST FRAMEWORK CONFIGURATION

########## AUTHENTICATION CONFIGURATION
#AUTH_USER_MODEL = 'main.User'
LOGIN_URL = reverse_lazy('auth_login')
########## END AUTHENTICATION CONFIGURATION

########## THUMBNAIL CONFIGURATION (used for cropping in admin)
#from easy_thumbnails.conf import Settings as thumbnail_settings
#THUMBNAIL_PROCESSORS = (
#    'image_cropping.thumbnail_processors.crop_corners',
#) + thumbnail_settings.THUMBNAIL_PROCESSORS
#
#IMAGE_CROPPING_THUMB_SIZE = (500, 500)
########## END THUMBNAIL CONFIGURATION

########## BLANC BASIC PAGES CONFIGURATION
PAGE_TEMPLATES = (
    ('pages/default_template.html', 'default'),
)
########## END BLANC BASIC PAGES CONFIGURATION

TEMPLATE_VISIBLE_SETTINGS = (
    'STATIC_URL',
)

########## WEDDINGPLANNER SPECIFIC SETTINGS

########## END WEDDINGPLANNER SPECIFIC SETTINGS

