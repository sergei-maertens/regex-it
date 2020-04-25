from django import template
from django.conf import settings

from ..conf import InvoicesConf

register = template.Library()


@register.inclusion_tag("invoices/tags/address.html")
def company_details(client=None):
    if client is not None:
        return {
            "client": client,
            "company_name": client.name,
            "company_address": [
                client.address,
                client.city,
                client.get_country_display(),
            ],
            "company_tax_identifier": client.vat,
        }

    config_keys = InvoicesConf._meta.names.items()
    return {name.lower(): getattr(settings, setting) for name, setting in config_keys}


@register.simple_tag
def company_field(prop):
    key = "INVOICES_COMPANY_%s" % prop
    return getattr(settings, key)
