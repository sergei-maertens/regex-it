from argparse import CommandParser

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Fetch the invoices for the specified date range"

    def add_arguments(self, parser: CommandParser) -> None:
        import bpdb

        bpdb.set_trace()

    def handle(self, **options) -> None:
        import bpdb

        bpdb.set_trace()
