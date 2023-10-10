from django.test import RequestFactory

import factory

from regex.crm.tests.factories import ClientFactory

from ..models import Invoice, InvoiceItem
from ..utils import render_invoice_pdf


def _generate_invoice_pdf(invoice: Invoice, create, extracted, **kwargs):
    invoice.generate()
    factory = RequestFactory()
    request = factory.get("/dummy")
    render_invoice_pdf(request, invoice=invoice)


class InvoiceFactory(factory.django.DjangoModelFactory):
    client = factory.SubFactory(ClientFactory)

    class Meta:
        model = Invoice

    class Params:
        with_pdf = factory.Trait(
            item=factory.RelatedFactory(
                "regex.invoices.tests.factories.InvoiceItemFactory",
                factory_related_name="invoice",
                amount=factory.Faker(
                    "pydecimal", left_digits=2, right_digits=2, min_value=1
                ),
                rate=0,
            ),
            _generate=factory.PostGeneration(_generate_invoice_pdf),
        )


class InvoiceItemFactory(factory.django.DjangoModelFactory):
    invoice = factory.SubFactory(InvoiceFactory)

    class Meta:
        model = InvoiceItem
