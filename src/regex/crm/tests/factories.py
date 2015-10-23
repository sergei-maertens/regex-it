import factory
import factory.fuzzy

from ..models import Client, Contact, Project


class SimpleSequence(factory.Sequence):

    def __init__(self, template, *args, **kwargs):
        def f(n):
            return template.format(n)
        super(SimpleSequence, self).__init__(f, *args, **kwargs)


class ClientFactory(factory.django.DjangoModelFactory):

    name = SimpleSequence('Client {}')
    email = SimpleSequence('client-{}@regex-it.nl')
    city = SimpleSequence('City-{}')
    phone = SimpleSequence('+316 229133{0}{0}')

    class Meta:
        model = Client


class ProjectFactory(factory.django.DjangoModelFactory):

    client = factory.SubFactory(ClientFactory)
    name = SimpleSequence('Project {}')

    base_rate = factory.fuzzy.FuzzyDecimal(50, 100)

    class Meta:
        model = Project


class ContactFactory(factory.django.DjangoModelFactory):

    label = SimpleSequence('Contact {}')
    name = SimpleSequence('Contact {}')
    email = SimpleSequence('contact-{}@regex-it.nl')
    phone = '+310622391837'

    class Meta:
        model = Contact
