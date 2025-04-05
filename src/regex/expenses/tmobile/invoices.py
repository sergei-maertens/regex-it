import asyncio
from datetime import date
from pathlib import Path
from typing import List

from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile

from asgiref.sync import sync_to_async

from ..fetcher import BaseInvoiceFetcher
from ..models import Invoice
from .scraper import main as download_tmobile_invoices


class InvoiceFetcher(BaseInvoiceFetcher):
    default_creditor_field = "tmobile_creditor"

    def __call__(self) -> List[Invoice]:
        existing_invoices = Invoice.objects.filter(creditor=self.get_default_creditor())
        invoices = []

        @sync_to_async(thread_sensitive=True)
        def handle_invoice_download(filepath: Path, comments: str):
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
                notes=comments,
                review_required=True,
                md5_hash=md5_hash,
                identifier=md5_hash,
                date=date.today(),
                amount=0,
                pdf=pdf,
            )
            invoices.append(invoice)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            download_tmobile_invoices(
                email=settings.TMOBILE_EMAIL,
                password=settings.TMOBILE_PASSWORD,
                on_mfa_prompt=lambda: input("Enter Odido MFA code: "),
                subscription_label=settings.TMOBILE_SUBSCRIPTION_LABEL,
                on_invoice_download=handle_invoice_download,
            )
        )

        return invoices
