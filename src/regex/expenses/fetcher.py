from dataclasses import dataclass, field
from datetime import date
from typing import List

from django.core.files.uploadedfile import TemporaryUploadedFile

from .models import ExpensesConfiguration, Invoice


@dataclass
class BaseInvoiceFetcher:
    config: ExpensesConfiguration
    start_date: date
    end_date: date  # inclusive!
    files: List[TemporaryUploadedFile] = field(init=False, default_factory=list)
    default_creditor_field: str = field(init=False, default="")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for file in self.files:
            file.close()

    def __call__(self) -> List[Invoice]:
        raise NotImplementedError("Subclasses must implement the __call__ method.")

    def get_default_creditor(self):
        if not self.default_creditor_field:
            return None
        return getattr(self.config, self.default_creditor_field)
