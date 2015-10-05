from django.contrib import admin

from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'due_date', 'received', 'created')
    list_filter = ('client', 'date', 'due_date', 'received')
    inlines = [InvoiceItemInline]
