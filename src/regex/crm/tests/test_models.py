from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import ProjectFactory


class ProjectTests(TestCase):
    def test_no_base_rate_or_fee(self):
        with self.assertRaises(ValidationError):
            ProjectFactory.create(base_rate=None, flat_fee=None)
