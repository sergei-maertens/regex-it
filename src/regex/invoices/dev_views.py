from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView

from .models import Invoice
from .utils import get_invoice_context


class InvoicePDFTestView(UserPassesTestMixin, DetailView):
    model = Invoice
    template_name = "invoices/invoice_detail.html"
    context_object_name = "invoice"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(**get_invoice_context(self.object, request=self.request))
        return context
