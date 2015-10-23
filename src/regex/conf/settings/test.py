import time
import tempfile

from .base import *

#
# Standard Django settings.
#

DEBUG = True
TEMPLATE_DEBUG = DEBUG
WSGI_APPLICATION = 'mijke.wsgi.wsgi_test.application'
ENVIRONMENT = 'test'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'TEST_NAME': 'test_regex_{0}'.format(time.time())
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

LOGGING['loggers'].update({
    'django': {
        'handlers': ['django'],
        'level': 'WARNING',
        'propagate': True,
    },
})


MEDIA_ROOT = tempfile.mkdtemp()
PRIVATE_MEDIA_ROOT = tempfile.mkdtemp()
