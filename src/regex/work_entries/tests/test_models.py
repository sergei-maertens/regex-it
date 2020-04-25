from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from .factories import WorkEntryFactory


class WorkEntryTests(TestCase):
    def test_delta_to_decimal(self):
        entry = WorkEntryFactory.create(
            start=datetime(2015, 9, 14, 8, 0).replace(tzinfo=timezone.utc),
            end=datetime(2015, 9, 14, 12, 0).replace(tzinfo=timezone.utc),
        )
        self.assertEqual(entry.delta_to_decimal(), Decimal(4))
