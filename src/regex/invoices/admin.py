from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from .models import Invoice, InvoiceItem


def generate_invoices(modeladmin, request, queryset):
    for invoice in queryset:
        invoice.generate()
generate_invoices.short_description = _("Generate invoice items")


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'due_date', 'received', 'created', 'n_items', 'generated')
    list_filter = ('client', 'date', 'due_date', 'received')
    inlines = [InvoiceItemInline]
    actions = [generate_invoices]

    def get_queryset(self, request=None):
        return super().get_queryset(request=request).annotate(n_items=Count('invoiceitem'))

    def n_items(self, obj):
        return obj.n_items
    n_items.short_description = _('# invoice items')
