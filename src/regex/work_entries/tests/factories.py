import factory

from regex.accounts.tests.factories import UserFactory
from regex.crm.tests.factories import ProjectFactory

from ..models import WorkEntry


class WorkEntryFactory(factory.django.DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = WorkEntry
