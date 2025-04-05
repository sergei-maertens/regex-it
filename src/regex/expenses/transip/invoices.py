from base64 import b64decode
from datetime import date
from decimal import Decimal
from typing import Literal

from django.core.files.uploadedfile import TemporaryUploadedFile

from pydantic import BaseModel
from requests import Session

from ..fetcher import BaseInvoiceFetcher
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

    def as_django_invoice(self, pdf: TemporaryUploadedFile) -> Invoice:
        assert self.currency == "EUR"
        return Invoice(
            identifier=self.invoice_number,
            date=self.creation_date,
            amount=Decimal(self.total_amount_incl_vat) / 100,
            pdf=pdf,
        )


def _get_invoice_list(
    url: str, session: Session, auth: TransipAuth
) -> tuple[list[TransipInvoice], str]:
    response = session.get(url, params={"pageSize": 18}, auth=auth)
    response.raise_for_status()
    data = response.json()
    invoices = [TransipInvoice(**attrs) for attrs in data["invoices"]]
    next_page = next(
        (link["link"] for link in data["_links"] if link["rel"] == "next"), ""
    )
    return invoices, next_page


def download_pdf(
    session: Session, auth: TransipAuth, invoice: TransipInvoice
) -> TemporaryUploadedFile:
    response = session.get(
        build_url(f"invoices/{invoice.invoice_number}/pdf"),
        auth=auth,
    )
    response.raise_for_status()
    pdf_b64 = response.json()["pdf"].encode("ascii")

    content = b64decode(pdf_b64 + b"==")
    temp_file = TemporaryUploadedFile(
        f"{invoice.invoice_number}.pdf", "application/pdf", len(content), charset=None
    )
    temp_file.write(content)
    temp_file.seek(0)
    return temp_file


class InvoiceFetcher(BaseInvoiceFetcher):
    default_creditor_field = "transip_creditor"

    def __call__(self) -> list[Invoice]:
        auth = TransipAuth()

        def _check_relevancy(invoice: TransipInvoice) -> bool:
            return self.start_date <= invoice.creation_date <= self.end_date

        with Session() as session:
            invoices, next_page = _get_invoice_list(
                build_url("invoices"), session, auth
            )

            # check if we need to fetch the next page
            while invoices and next_page and _check_relevancy(invoices[-1]):
                next_page_invoices, next_page = _get_invoice_list(
                    next_page, session, auth
                )
                invoices += next_page_invoices

        invoices = [invoice for invoice in invoices if _check_relevancy(invoice)]
        self.files = [download_pdf(session, auth, invoice) for invoice in invoices]
        return [
            invoice.as_django_invoice(pdf) for invoice, pdf in zip(invoices, self.files)
        ]
