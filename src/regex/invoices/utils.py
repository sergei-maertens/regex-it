"""
Utility functions for invoices.
"""
from io import BytesIO

from django.core.files import File
from django.db.models import Count
from django.template import loader, RequestContext

import weasyprint
from sendfile import sendfile

from regex.utils.pdf import UrlFetcher
from regex.utils.views.pdf import PDFTemplateResponse, PDFTemplateResponseMixin


def render_invoice_pdf(request, invoice, template_name='invoices/invoice_detail.html'):
    if isinstance(template_name, (list, tuple)):
        template = loader.select_template(template_name)
    else:
        template = loader.get_template(template_name)

    tax_rates = invoice.invoiceitem_set.values('tax_rate').annotate(num=Count('tax_rate'))
    context = {
        'invoice': invoice,
        'tax_rates': tax_rates,
        'items': invoice.invoiceitem_set.select_related('project').order_by('project', 'tax_rate')
    }
    html = template.render(RequestContext(request, context))
    base_url = request.build_absolute_uri("/")
    url_fetcher = UrlFetcher(request, base_url)
    wp = weasyprint.HTML(string=html, base_url=base_url, url_fetcher=url_fetcher)
    # pdf as bytes
    buffer = BytesIO()
    wp.write_pdf(target=buffer)
    filename = '{}.pdf'.format(invoice.invoice_number)
    invoice.pdf.save(filename, File(buffer))


class InvoicePDFTemplateResponse(PDFTemplateResponse):

    def __init__(self, invoice=None, *args, **kwargs):
        self.invoice = invoice
        super(InvoicePDFTemplateResponse, self).__init__(*args, **kwargs)

    @property
    def rendered_content(self):
        """
        Read the invoices pdf, or generate it and return the rendered pdf.
        """
        assert self.invoice is not None

        if not self.invoice.pdf:
            render_invoice_pdf(self._request, self.invoice, template_name=self.template_name)
        return self.invoice.pdf.read()


class InvoicePDFTemplateResponseMixin(PDFTemplateResponseMixin):

    response_class = InvoicePDFTemplateResponse

    def render_to_response(self, *args, **kwargs):
        # if the pdf exists, use sendfile
        if self.object.pdf:
            return sendfile(
                self.request, self.object.pdf.path,
                attachment=True, attachment_filename=self.get_filename()
            )
        kwargs['invoice'] = self.object
        return super(InvoicePDFTemplateResponseMixin, self).render_to_response(*args, **kwargs)
