from import_export import resources

from .models import InvoiceItem


class InvoiceItemResource(resources.ModelResource):
    class Meta:
        model = InvoiceItem
        fields = ("id", "invoice", "project", "rate", "amount", "tax_rate")
