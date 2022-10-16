from datetime import date

from django.core.management import BaseCommand, CommandError

from dateutil.relativedelta import relativedelta

from ...transip.service import fetch_invoices


class Command(BaseCommand):
    help = "Fetch the invoices for the specified date range"

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

        all_invoices = []
        all_invoices += fetch_invoices(start_date, end_date)

        # TODO - ensure duplicates are not stored again
        # TODO - store creditor per provider in admin/config and assign here
        import bpdb

        bpdb.set_trace()
