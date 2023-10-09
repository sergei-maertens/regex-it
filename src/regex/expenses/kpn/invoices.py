import asyncio
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import List

from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile

from asgiref.sync import sync_to_async

from ..fetcher import BaseInvoiceFetcher
from ..models import Invoice
from .scraper import main as download_kpn_invoices


class InvoiceFetcher(BaseInvoiceFetcher):
    default_creditor_field = "kpn_creditor"

    def __call__(self) -> List[Invoice]:
        existing_invoices = Invoice.objects.filter(creditor=self.get_default_creditor())
        invoices = []

        @sync_to_async(thread_sensitive=True)
        def handle_invoice_download(
            filepath: Path, invoice_date: date, amount: Decimal
        ):
            with filepath.open("rb") as invoice_file:
                md5_hash = Invoice.calculate_hash(invoice_file)
                if existing_invoices.filter(md5_hash=md5_hash).exists():
                    return

                invoice_file.seek(0)
                pdf = TemporaryUploadedFile(
                    f"{filepath.name}.pdf",
                    "application/pdf",
                    filepath.stat().st_size,
                    charset=None,
                )
                pdf.write(invoice_file.read())
                pdf.seek(0)

            self.files.append(pdf)
            invoice = Invoice(
                notes="From scraping",
                review_required=True,
                md5_hash=md5_hash,
                identifier=md5_hash,
                date=invoice_date,
                amount=amount,
                pdf=pdf,
            )
            invoices.append(invoice)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            download_kpn_invoices(
                email=settings.KPN_EMAIL,
                password=settings.KPN_PASSWORD,
                start=self.start_date,
                end=self.end_date,
                on_invoice_download=handle_invoice_download,
            )
        )

        return invoices
