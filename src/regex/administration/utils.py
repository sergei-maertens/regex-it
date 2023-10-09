from dataclasses import dataclass
from datetime import date

from dateutil.relativedelta import relativedelta


@dataclass
class DateRange:
    start: date
    end: date


def _get_quarter(offset: int = 0) -> DateRange:
    # offset: 0 = current quarter
    # offset: -1 = previous quarter
    today = date.today()
    months_to_subtract = (today.month - 1) % 3 - (offset * 3)
    start_date = (today - relativedelta(months=months_to_subtract)).replace(day=1)
    end_date = start_date + relativedelta(months=3, days=-1)
    return DateRange(start=start_date, end=end_date)


def get_current_quarter() -> DateRange:
    return _get_quarter(offset=0)


def get_previous_quarter() -> DateRange:
    return _get_quarter(offset=-1)
