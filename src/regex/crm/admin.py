from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from regex.utils.admin.decorators import link_list

from .models import Client, Contact, Project


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("label", "name", "email", "phone", "clients")
    list_filter = ("client",)

    def get_queryset(self, request=None):
        base = super(ContactAdmin, self).get_queryset(request=request)
        return base.prefetch_related("client_set")

    @link_list(short_description=_("clients"))
    def clients(self, obj):
        return obj.client_set.all()


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "city", "country", "get_contacts")
    list_filter = ("created", "modified")
    search_fields = ("name", "email", "contacts__name")
    filter_horizontal = ("contacts",)

    def get_queryset(self, request=None):
        base = super(ClientAdmin, self).get_queryset(request=request)
        return base.prefetch_related("contacts", "project_set")

    @link_list(short_description=_("contacts"))
    def get_contacts(self, obj):
        return obj.contacts.all()

    @link_list(short_description=_("projects"))
    def get_projects(self, obj):
        return obj.project_set.all()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "base_rate", "flat_fee", "tax_rate")
    list_filter = ("client",)
    search_fields = ("name",)
