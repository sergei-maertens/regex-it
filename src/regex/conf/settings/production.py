import os

from .base import *

#
# Standard Django settings.
#

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ENVIRONMENT = "production"

ADMINS = (("Sergei Maertens", "info@regex-it.nl"),)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "localhost",
    }
}

SECRET_KEY = os.getenv("SECRET_KEY")

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "regex-it.nl", "www.regex-it.nl"]

LOGGING["loggers"].update(
    {"django": {"handlers": ["django"], "level": "WARNING", "propagate": True,},}
)

#
# django-maintenancemode
#
MAINTENANCE_MODE = False

#
# Invoices
#
INVOICES_COMPANY_NAME = os.getenv("COMPANY_NAME")
INVOICES_COMPANY_ADDRESS = (os.getenv("COMPANY_ADDRESS") or "").split(",")
INVOICES_COMPANY_TAX_IDENTIFIER = os.getenv("COMPANY_TAX_IDENTIFIER")
INVOICES_COMPANY_KVK = os.getenv("COMPANY_KVK")
INVOICES_COMPANY_IBAN = os.getenv("COMPANY_IBAN")
