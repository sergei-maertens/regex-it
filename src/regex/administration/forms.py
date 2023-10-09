import zipfile
from dataclasses import dataclass
from typing import BinaryIO

from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from regex.expenses.models import Invoice as DebitInvoice
from regex.invoices.models import Invoice as CreditInvoice


class ExportQuarterChoices(models.TextChoices):
    previous = "previous", _("Previous")
    current = "current", _("Current")


@dataclass
class ExportData:
    credit: list[CreditInvoice]
    debit: list[DebitInvoice]

    def write_zip(self, outfile: BinaryIO):
        with zipfile.ZipFile(outfile, "w") as archive:
            archive.mkdir("credit")
            archive.mkdir("debit")


class ExportAdministrationForm(forms.Form):
    quarter = forms.ChoiceField(
        label=_("Quarter"),
        help_text=_("Which quarter to export."),
        choices=lambda: ExportQuarterChoices.choices,
        required=False,
    )
    start = forms.DateField(
        label=_("Start"),
        help_text=_("Export from this date."),
        required=False,
    )
    end = forms.DateField(
        label=_("End"),
        help_text=_("Export until (including) this date."),
        required=False,
    )

    def prepare_export_date(self) -> ExportData:
        return ExportData(
            credit=[],
            debit=[],
        )
