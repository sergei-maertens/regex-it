import os

from .base import *

#
# Standard Django settings.
#

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ENVIRONMENT = 'staging'

ADMINS = (
    ('Sergei Maertens', 'info@regex-it.nl'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
    }
}

SECRET_KEY = os.getenv('SECRET_KEY')

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', 'staging.regex-it.nl', 'www.staging.regex-it.nl']

LOGGING['loggers'].update({
    'django': {
        'handlers': ['django'],
        'level': 'WARNING',
        'propagate': True,
    },
})

#
# django-maintenancemode
#
MAINTENANCE_MODE = False
