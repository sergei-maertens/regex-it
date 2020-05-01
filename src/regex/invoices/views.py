from django.db.models import Count
from django.views.generic import DetailView

from rules.contrib.views import PermissionRequiredMixin

from .models import Invoice
from .utils import InvoicePDFTemplateResponseMixin


class InvoiceDetailView(PermissionRequiredMixin, DetailView):
    model = Invoice
    queryset = Invoice.objects.select_related('client').annotate(n_items=Count('invoiceitem'))
    slug_field = 'invoice_number'
    slug_url_kwarg = 'invoice_number'
    context_object_name = 'invoice'
    permission_required = 'invoices.can_view_invoice'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        tax_rates = self.object.invoiceitem_set.values('tax_rate').annotate(num=Count('tax_rate'))
        context.update({
            'tax_rates': tax_rates,
            'items': self.object.invoiceitem_set.select_related('project').order_by('date', 'project', 'tax_rate')
        })
        return context


class InvoiceDetailPDFView(InvoicePDFTemplateResponseMixin, InvoiceDetailView):

    def get_filename(self):
        return '{}.pdf'.format(self.object.invoice_number)
