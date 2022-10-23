from django.contrib import admin

from privates.admin import PrivateMediaMixin
from solo.admin import SingletonModelAdmin

from .models import Creditor, ExpensesConfiguration, Invoice


@admin.register(Creditor)
class CreditorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Invoice)
class InvoiceAdmin(PrivateMediaMixin, admin.ModelAdmin):
    list_display = ("identifier", "date", "amount", "creditor")
    list_select_related = ("creditor",)
    search_fields = ("identifier",)
    date_hierarchy = "date"
    private_media_fields = ("pdf",)


@admin.register(ExpensesConfiguration)
class ExpensesConfigurationAdmin(SingletonModelAdmin):
    pass
