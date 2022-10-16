from django.contrib import admin

from .models import Creditor, Invoice


@admin.register(Creditor)
class CreditorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("identifier", "date", "amount", "creditor")
    list_select_related = ("creditor",)
    search_fields = ("identifier",)
    date_hierarchy = "date"
