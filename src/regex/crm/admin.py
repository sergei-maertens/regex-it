from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Contact, Client
from regex.utils.admin.decorators import link_list


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'email', 'phone', 'clients')
    list_filter = ('client',)

    def get_queryset(self, request=None):
        base = super(ContactAdmin, self).get_queryset(request=request)
        return base.prefetch_related('client_set')

    @link_list(short_description=_('clients'))
    def clients(self, obj):
        return obj.client_set.all()


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'country', 'get_contacts')
    list_filter = ('created', 'modified')
    search_fields = ('name', 'email', 'contacts__name')
    filter_horizontal = ('contacts',)

    def get_queryset(self, request=None):
        base = super(ClientAdmin, self).get_queryset(request=request)
        return base.prefetch_related('contacts')

    @link_list(short_description=_('contacts'))
    def get_contacts(self, obj):
        return obj.contacts.all()
