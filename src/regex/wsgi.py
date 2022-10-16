"""
WSGI config for regex project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application


def setupenv():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path = [src_dir] + sys.path


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "regex.conf.settings")

setupenv()
application = get_wsgi_application()
