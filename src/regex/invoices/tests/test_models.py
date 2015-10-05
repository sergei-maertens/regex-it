from datetime import datetime, date

from django.test import TestCase
from django.utils import timezone

from freezegun import freeze_time

from regex.crm.tests.factories import ClientFactory, ProjectFactory
from regex.work_entries.tests.factories import WorkEntryFactory
from ..models import InvoiceItem
from .factories import InvoiceFactory


class InvoiceTests(TestCase):

    @freeze_time('2015-10-02')
    def test_pickup_work_entries(self):
        """
        Test that the work entries are correctly picked up for a given invoice date.
        """
        client1, client2 = ClientFactory.create_batch(2)
        project1, project2 = ProjectFactory.create_batch(2, client=client1)
        project3 = ProjectFactory.create(client=client2)

        # worked a bit on project 1
        WorkEntryFactory.create(
            project=project1,
            start=datetime(2015, 9, 14, 8, 0).replace(tzinfo=timezone.utc),
            end=datetime(2015, 9, 14, 12, 0).replace(tzinfo=timezone.utc)
        )

        # worked a bit on project 2
        WorkEntryFactory.create(
            project=project2,
            start=datetime(2015, 9, 14, 13, 0).replace(tzinfo=timezone.utc),
            end=datetime(2015, 9, 14, 15, 30).replace(tzinfo=timezone.utc)
        )
        WorkEntryFactory.create(
            project=project2,
            start=datetime(2015, 9, 30, 13, 0).replace(tzinfo=timezone.utc),
            end=datetime(2015, 9, 30, 15, 30).replace(tzinfo=timezone.utc)
        )

        # future entry to be ignored
        WorkEntryFactory.create(
            project=project1,
            start=datetime(2015, 10, 1, 8, 0).replace(tzinfo=timezone.utc),
            end=datetime(2015, 10, 1, 11, 0).replace(tzinfo=timezone.utc)
        )

        # different client
        WorkEntryFactory.create(
            project=project3,
            start=datetime(2015, 9, 21, 8, 0).replace(tzinfo=timezone.utc),
            end=datetime(2015, 9, 21, 11, 0).replace(tzinfo=timezone.utc)
        )

        # create the invoices
        invoice1 = InvoiceFactory.create(client=client1, date=date(2015, 9, 30))
        invoice2 = InvoiceFactory.create(client=client1, date=date(2015, 10, 31))

        # generate the invoices and check that the correct number of lines are created
        invoice1.generate()
        self.assertEqual(InvoiceItem.objects.count(), 3)

        invoice2.generate()
        self.assertEqual(InvoiceItem.objects.count(), 4)
