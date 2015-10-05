import factory

from regex.crm.tests.factories import ClientFactory
from ..models import Invoice


class InvoiceFactory(factory.django.DjangoModelFactory):

    client = factory.SubFactory(ClientFactory)

    class Meta:
        model = Invoice
