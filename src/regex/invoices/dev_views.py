from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView

from .models import Invoice


class InvoicePDFTestView(UserPassesTestMixin, DetailView):
    model = Invoice
    template_name = "invoices/invoice_detail.html"
    context_object_name = "invoice"

    def test_func(self):
        return self.request.user.is_superuser
