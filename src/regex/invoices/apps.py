from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InvoicesConfig(AppConfig):
    name = "regex.invoices"
    verbose_name = _("Invoices")

    def ready(self):
        from . import rules  # noqa
