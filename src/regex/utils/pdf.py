import mimetypes
import posixpath
import urllib
from io import BytesIO

from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import FileSystemStorage, staticfiles_storage

import weasyprint


class UrlFetcher(object):

    """
    URL fetcher that skips the network for /static/* files.
    """

    fallback = weasyprint.default_url_fetcher

    def __init__(self, request, base_url=None):
        self.request = request
        # build the static url to look for
        static_url = urllib.parse.urlsplit(settings.STATIC_URL)
        if not static_url.scheme and not static_url.netloc:
            static_url = urllib.parse.urljoin(base_url, settings.STATIC_URL)
            static_url = urllib.parse.urlsplit(static_url)
        self.static_url = static_url
        self.local_storage = issubclass(staticfiles_storage.__class__, FileSystemStorage)

    def __call__(self, url):
        orig_url = url
        url = urllib.parse.urlsplit(url)
        same_base = (self.static_url.scheme, self.static_url.netloc) == (url.scheme, url.netloc)
        if self.local_storage and same_base and url.path.startswith(self.static_url.path):
            path = url.path.replace(self.static_url.path, '')
            normalized_path = posixpath.normpath(urllib.parse.unquote(path)).lstrip('/')
            absolute_path = finders.find(normalized_path)
            content_type, encoding = mimetypes.guess_type(absolute_path)
            result = dict(
                mime_type=content_type,
                encoding=encoding,
                redirected_url=orig_url
            )
            with open(absolute_path, 'rb') as f:
                result['file_obj'] = BytesIO(f.read())
            return result
        return self.fallback(orig_url)
