from datetime import date
from decimal import Decimal
from typing import List, Literal, Tuple

from pydantic import BaseModel
from requests import Session

from ..models import Invoice
from .tokens import TransipAuth
from .utils import build_url


def to_camel(string: str) -> str:
    bits = string.split("_")
    camelized = "".join(word.capitalize() for word in bits[1:])
    return f"{bits[0]}{camelized}"


class TransipInvoice(BaseModel):
    invoice_number: str
    creation_date: date
    due_date: date
    currency: Literal["EUR"]
    total_amount: int
    total_amount_incl_vat: int

    class Config:
        alias_generator = to_camel

    def as_django_invoice(self) -> Invoice:
        assert self.currency == "EUR"
        return Invoice(
            identifier=self.invoice_number,
            date=self.creation_date,
            amount=Decimal(self.total_amount) / 100,
        )


def _get_invoice_list(
    url: str, session: Session, auth: TransipAuth
) -> Tuple[List[TransipInvoice], str]:
    response = session.get(url, params={"pageSize": 18}, auth=auth)
    response.raise_for_status()
    data = response.json()
    invoices = [TransipInvoice(**attrs) for attrs in data["invoices"]]
    next_page = next(
        (link["link"] for link in data["_links"] if link["rel"] == "next"), ""
    )
    return invoices, next_page


def fetch_invoices(start_date: date, end_date: date) -> List[Invoice]:
    auth = TransipAuth()

    def _check_relevancy(invoice: TransipInvoice) -> bool:
        return start_date <= invoice.creation_date <= end_date

    with Session() as session:
        invoices, next_page = _get_invoice_list(build_url("invoices"), session, auth)

        # check if we need to fetch the next page
        while invoices and next_page and _check_relevancy(invoices[-1]):
            next_page_invoices, next_page = _get_invoice_list(next_page, session, auth)
            invoices += next_page_invoices

    # TODO: download PDFs for relevant invoices
    invoices = [invoice for invoice in invoices if _check_relevancy(invoice)]
    return [invoice.as_django_invoice() for invoice in invoices]
