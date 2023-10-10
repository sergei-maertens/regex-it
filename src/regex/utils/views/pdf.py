from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin, TemplateView

import weasyprint

from ..pdf import UrlFetcher


class PDFTemplateResponse(TemplateResponse):
    url_fetcher_class = UrlFetcher

    def __init__(self, filename=None, *args, **kwargs):
        kwargs["content_type"] = "application/pdf"
        super(PDFTemplateResponse, self).__init__(*args, **kwargs)
        if filename:
            self["Content-Disposition"] = 'attachment; filename="%s"' % filename
        else:
            self["Content-Disposition"] = "attachment"

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
        kwargs["filename"] = self.get_filename()
        return super(PDFTemplateResponseMixin, self).render_to_response(*args, **kwargs)


class PDFTemplateView(TemplateView, PDFTemplateResponseMixin):
    pass
