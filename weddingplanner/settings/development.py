"""
Development settings.
"""
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.debug',
)

INSTALLED_APPS += (
   'debug_toolbar',
    'django_extensions',
    'django_nose'
)

LOGGING['loggers']['weddingplanner'] = {
    'handlers': ['console'],
    'level': 'DEBUG'
}

LOGGING['formatters']['verbose']['()'] = 'coloredlogs.ColoredFormatter'

# NOTE: the below enforces http authentication (will return a 401)
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'rest_framework.authentication.BasicAuthentication',) + REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']

REST_FRAMEWORK['TEST_REQUEST_DEFAULT_FORMAT'] = 'json'

# Test settings
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--all-modules',
    '--with-yanc',
    '--verbosity=2'
]

# NOSE_PLUGINS = []

# Sent mail is saved in files (rather than actually being sent) in development mode
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'tests/sent_mail'
# Optionally you can send email to the console (add the below line to local.py, don't edit this
# file)
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MINIFIED_JS = False

DEBUG_TOOLBAR_CONFIG = {
    # Provide our own local version here so that we can use the toolbar even when offline
    'JQUERY_URL': STATIC_URL + 'js/vendor/jquery-1.11.0.min.js',
    'SHOW_TEMPLATE_CONTEXT': True,

}

# Raven/Sentry -- please insert your raven config into local.py. Template below. Remember to append
#  verify_ssl=0 at the end as we don't have a RootCA signed certificate on the server yet.
#
#RAVEN_CONFIG = {
#    'dsn': 'https://..../?verify_ssl=0',
#}

# TODO: FILL!
ALLOWED_HOSTS = []

try:
    from .local import *
except ImportError:
    # local settings is not mandatory
    pass
