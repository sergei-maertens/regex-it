from datetime import date

from django.core.management import BaseCommand, CommandError
from django.db import transaction

from dateutil.relativedelta import relativedelta

from ...models import ExpensesConfiguration, Invoice
from ...transip.service import InvoiceFetcher as TransipInvoiceFetcher


class Command(BaseCommand):
    help = "Fetch the invoices for the specified date range"
    output_transaction = True

    def add_arguments(self, parser) -> None:
        parser.add_argument("--current-quarter", action="store_true")
        parser.add_argument(
            "--start-date",
            type=date.fromisoformat,
            help="Fetch invoices dated from this date.",
        )
        parser.add_argument(
            "--end-date",
            type=date.fromisoformat,
            help="Fetch invoices dated until (and including) this date.",
        )

    @transaction.atomic()
    def handle(self, **options) -> None:
        start_date = options["start_date"]
        end_date = options["end_date"]
        current_quarter = options["current_quarter"]

        if current_quarter and (start_date or end_date):
            raise CommandError(
                "--current-quarter is mutually exclusive with start or end date."
            )
        elif not current_quarter and not (start_date and end_date):
            raise CommandError(
                "Both --start-date and --end-date are required if one option is used."
            )

        if current_quarter:
            today = date.today()
            months_to_subtract = (today.month - 1) % 3
            start_date = (today - relativedelta(months=months_to_subtract)).replace(
                day=1
            )
            end_date = start_date + relativedelta(months=3, days=-1)

        config = ExpensesConfiguration.get_solo()
        fetchers = [TransipInvoiceFetcher]
        counter = 0

        for fetcher_cls in fetchers:
            fetcher = fetcher_cls(
                config=config, start_date=start_date, end_date=end_date
            )
            with fetcher:
                _creditor = fetcher.get_default_creditor()
                invoices = fetcher()
                # only keep invoices that don't exist yet
                _identifiers = [invoice.identifier for invoice in invoices]
                existing_identifiers = set(
                    Invoice.objects.filter(identifier__in=_identifiers).values_list(
                        "identifier", flat=True
                    )
                )
                for invoice in invoices:
                    if invoice.identifier in existing_identifiers:
                        continue
                    invoice.creditor = _creditor
                    invoice.save()
                    counter += 1

        if counter == 0:
            self.stdout.write("No new invoices saved.")
        else:
            self.stdout.write(self.style.SUCCESS(f"Saved {counter} invoice(s)."))
