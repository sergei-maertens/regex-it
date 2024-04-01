from datetime import date

from django.core.management import BaseCommand, CommandError
from django.db import transaction

from regex.administration.utils import (
    DateRange,
    get_current_quarter,
    get_previous_quarter,
)

from ...kpn.service import InvoiceFetcher as KPNInvoiceFetcher
from ...models import ExpensesConfiguration, Invoice
from ...tmobile.service import InvoiceFetcher as TMobileInvoiceFetcher
from ...transip.service import InvoiceFetcher as TransipInvoiceFetcher

FETCHERS = [
    TransipInvoiceFetcher,
    TMobileInvoiceFetcher,
    KPNInvoiceFetcher,
]


class Command(BaseCommand):
    help = "Fetch the invoices for the specified date range"
    output_transaction = True

    def add_arguments(self, parser) -> None:
        parser.add_argument("--previous-quarter", action="store_true")
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
        parser.add_argument(
            "--creditor",
            nargs="*",
            help=(
                "Fetch invoices only for these creditors. Possible values are: "
                + ", ".join(
                    field for f in FETCHERS if (field := f.default_creditor_field)
                )
            ),
        )

    @transaction.atomic()
    def handle(self, *args, **options) -> None:
        start_date = options["start_date"]
        end_date = options["end_date"]
        previous_quarter = options["previous_quarter"]
        current_quarter = options["current_quarter"]
        creditors = options["creditor"]

        if (current_quarter or previous_quarter) and (start_date or end_date):
            raise CommandError(
                "--current-quarter/--previousquarter is mutually exclusive with "
                "start or end date."
            )
        elif not (current_quarter or previous_quarter) and not (
            start_date and end_date
        ):
            raise CommandError(
                "Both --start-date and --end-date are required if one option is used."
            )

        if previous_quarter:
            date_range = get_previous_quarter()
        elif current_quarter:
            date_range = get_current_quarter()
        else:
            date_range = DateRange(start=start_date, end=end_date)

        self.stdout.write(
            f"Looking for invoices between {date_range.start.isoformat()} "
            f"and {date_range.end.isoformat()}"
        )

        config = ExpensesConfiguration.get_solo()
        counter = 0

        for fetcher_cls in FETCHERS:
            if creditors and fetcher_cls.default_creditor_field not in creditors:
                continue
            fetcher = fetcher_cls(
                config=config, start_date=date_range.start, end_date=date_range.end
            )
            with fetcher:
                _creditor = fetcher.get_default_creditor()
                self.stdout.write(f"Getting invoices for: {_creditor}")

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
