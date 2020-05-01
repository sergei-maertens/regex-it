import factory

from regex.crm.tests.factories import ClientFactory

from ..models import Invoice, InvoiceItem


class InvoiceFactory(factory.django.DjangoModelFactory):

    client = factory.SubFactory(ClientFactory)

    class Meta:
        model = Invoice


class InvoiceItemFactory(factory.django.DjangoModelFactory):

    invoice = factory.SubFactory(InvoiceFactory)

    class Meta:
        model = InvoiceItem
