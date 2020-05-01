from django import template

from regex.config.models import CompanyConfig

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

    config = CompanyConfig.get_solo()
    return {
        "company_name": config.company_name,
        "company_address": config.company_address,
        "company_tax_identifier": config.tax_identifier,
        "company_coc": config.coc,
        "company_iban": config.iban,
    }
