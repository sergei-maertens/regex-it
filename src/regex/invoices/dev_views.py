from django.utils import translation
from django.views.generic import DetailView

from regex.administration.views import SuperUserRequired

from .models import Invoice
from .utils import get_invoice_context


class InvoicePDFTestView(SuperUserRequired, DetailView):
    model = Invoice
    template_name = "invoices/invoice_detail.html"
    context_object_name = "invoice"

    def get(self, request, *args, **kwargs):
        invoice = self.get_object()
        lang_code = invoice.client.language
        with translation.override(lang_code):
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(**get_invoice_context(self.object, request=self.request))
        return context
