from datetime import date

from django.test import SimpleTestCase

from freezegun import freeze_time

from ..utils import get_current_quarter, get_previous_quarter


class QuarterCalculationTests(SimpleTestCase):
    def test_current_quarter(self):
        cases = (
            ("2023-08-10", date(2023, 7, 1), date(2023, 9, 30)),
            ("2021-01-01", date(2021, 1, 1), date(2021, 3, 31)),
            ("2021-06-30", date(2021, 4, 1), date(2021, 6, 30)),
        )
        for today, start, end in cases:
            with (
                self.subTest(today=today, start=start, end=end),
                freeze_time(today),
            ):
                result = get_current_quarter()

                self.assertEqual(result.start, start)
                self.assertEqual(result.end, end)

    def test_previous_quarter(self):
        cases = (
            ("2023-08-10", date(2023, 4, 1), date(2023, 6, 30)),
            ("2021-01-01", date(2020, 10, 1), date(2020, 12, 31)),
            ("2021-06-30", date(2021, 1, 1), date(2021, 3, 31)),
        )
        for today, start, end in cases:
            with (
                self.subTest(today=today, start=start, end=end),
                freeze_time(today),
            ):
                result = get_previous_quarter()

                self.assertEqual(result.start, start)
                self.assertEqual(result.end, end)
