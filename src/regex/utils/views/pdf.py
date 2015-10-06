import mimetypes
import posixpath
import urllib

from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage, FileSystemStorage
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin, TemplateView

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
            with open(absolute_path, 'r') as f:
                output = f.read()
            return dict(
                string=output,
                mime_type=content_type,
                encoding=encoding,
                redirected_url=orig_url
            )
        return self.fallback(orig_url)


class PDFTemplateResponse(TemplateResponse):

    url_fetcher_class = UrlFetcher

    def __init__(self, filename=None, *args, **kwargs):
        kwargs['content_type'] = "application/pdf"
        super(PDFTemplateResponse, self).__init__(*args, **kwargs)
        if filename:
            self['Content-Disposition'] = 'attachment; filename="%s"' % filename
        else:
            self['Content-Disposition'] = 'attachment'

    def get_url_fetcher(self, base_url):
        return self.url_fetcher_class(self._request, base_url=base_url)

    @property
    def rendered_content(self):
        """
        Returns the rendered pdf
        """
        html = super(PDFTemplateResponse, self).rendered_content
        base_url = self._request.build_absolute_uri("/")
        url_fetcher = self.get_url_fetcher(base_url)
        wp = weasyprint.HTML(string=html, base_url=base_url, url_fetcher=url_fetcher)
        pdf = wp.write_pdf()
        return pdf


class PDFTemplateResponseMixin(TemplateResponseMixin):
    response_class = PDFTemplateResponse
    filename = None

    def get_filename(self):
        """
        Returns the filename of the rendered PDF.
        """
        return self.filename

    def render_to_response(self, *args, **kwargs):
        """
        Returns a response, giving the filename parameter to PDFTemplateResponse.
        """
        kwargs['filename'] = self.get_filename()
        return super(PDFTemplateResponseMixin, self).render_to_response(*args, **kwargs)


class PDFTemplateView(TemplateView, PDFTemplateResponseMixin):
    pass
