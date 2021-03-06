from .base import *

#
# Standard Django settings.
#

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ENVIRONMENT = "staging"

ADMINS = (("Sergei Maertens", "info@regex-it.nl"),)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "staging.regex-it.nl", "www.staging.regex-it.nl"]

LOGGING["loggers"].update(
    {"django": {"handlers": ["django"], "level": "WARNING", "propagate": True,},}
)
