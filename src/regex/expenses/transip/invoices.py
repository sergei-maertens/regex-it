from datetime import date
from typing import List

from ..models import Invoice


def fetch_invoices(start_date: date, end_date: date) -> List[Invoice]:
    import bpdb

    bpdb.set_trace()
