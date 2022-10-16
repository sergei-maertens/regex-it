from datetime import date
from typing import List

from requests import Session

from ..models import Invoice
from .tokens import create_access_token
from .utils import build_url


def fetch_invoices(start_date: date, end_date: date) -> List[Invoice]:
    with Session() as session:
        create_access_token(session)

        response = session.get(build_url("api-test"))
        response.raise_for_status()
