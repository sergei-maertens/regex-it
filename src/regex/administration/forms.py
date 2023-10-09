import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from regex.expenses.models import Invoice as DebitInvoice
from regex.invoices.models import Invoice as CreditInvoice

from .utils import DateRange, get_current_quarter, get_previous_quarter


class ExportQuarterChoices(models.TextChoices):
    previous = "previous", _("Previous")
    current = "current", _("Current")
    none = "", _("None")


@dataclass
class ExportData:
    credit: list[CreditInvoice]
    debit: list[DebitInvoice]

    def write_zip(self, outfile: BinaryIO):
        with zipfile.ZipFile(outfile, "w") as archive:
            archive.mkdir("credit")
            for invoice in self.credit:
                pdf_path = Path(invoice.pdf.path)
                archive.write(pdf_path, Path("credit") / pdf_path.name)

            archive.mkdir("debit")
            for invoice in self.debit:
                pdf_path = Path(invoice.pdf.path)
                archive.write(pdf_path, Path("debit") / pdf_path.name)


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

    def clean(self):
        quarter = self.cleaned_data.get("quarter")
        start = self.cleaned_data.get("start")
        end = self.cleaned_data.get("end")

        if not quarter or quarter == "none":
            if not start or not end:
                raise forms.ValidationError(
                    _("Specify a quarter or start and end date")
                )

        match quarter:
            case "previous":
                date_range = get_previous_quarter()
            case "current":
                date_range = get_current_quarter()
            case "none":
                date_range = DateRange(start=start, end=end)

        self.cleaned_data["date_range"] = date_range

        return self.cleaned_data

    def prepare_export_date(self) -> ExportData:
        date_range = self.cleaned_data["date_range"]
        debit = DebitInvoice.objects.filter(
            date__gte=date_range.start,
            date__lte=date_range.end,
        )
        credit = CreditInvoice.objects.filter(
            date__gte=date_range.start,
            date__lte=date_range.end,
        )
        return ExportData(
            credit=list(credit),
            debit=list(debit),
        )
