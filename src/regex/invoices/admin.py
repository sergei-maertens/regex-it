from django.contrib import admin
from django.urls import reverse
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from privates.admin import PrivateMediaMixin

from .forms import AdminInvoiceForm
from .models import Invoice, InvoiceItem
from .utils import render_invoice_pdf


def generate_invoices(modeladmin, request, queryset):
    for invoice in queryset:
        invoice.generate()


generate_invoices.short_description = _("Generate invoice details")


def render_pdf(modeladmin, request, queryset):
    for invoice in queryset:
        render_invoice_pdf(request, invoice)


render_pdf.short_description = _("Generate invoice pdfs")


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    raw_id_fields = ("project",)


@admin.register(Invoice)
class InvoiceAdmin(PrivateMediaMixin, admin.ModelAdmin):
    form = AdminInvoiceForm
    list_display = ('client', 'date', 'due_date', 'received', 'invoice_number',
                    'created', 'n_items', 'generated', 'invoice_items')
    list_filter = ('client', 'date', 'due_date', 'received')
    search_fields = ('invoice_number',)
    inlines = [InvoiceItemInline]
    actions = [generate_invoices, render_pdf]
    private_media_fields = ("pdf",)
    private_media_permission_required = "invoices.can_view_invoice"

    def get_queryset(self, request=None):
        qs = super().get_queryset(request=request)
        return qs.annotate(n_items=Count('invoiceitem'))

    def n_items(self, obj):
        return obj.n_items
    n_items.short_description = _('# invoice items')

    def invoice_items(self, obj):
        url = reverse('admin:invoices_invoiceitem_changelist')
        return format_html(
            '<a href="{}?invoice={}">{}</a>',
            url,
            obj.pk,
            _('invoice items'),
        )
    invoice_items.short_description = _('invoice items')


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'project', 'rate', 'amount', 'tax_rate')
    list_filter = ('invoice__client', 'project')
