from django.db import models
from django.utils.translation import gettext_lazy as _

from privates.fields import PrivateMediaFileField


class Creditor(models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("creditor")
        verbose_name_plural = _("creditors")

    def __str__(self):
        return self.name


class Invoice(models.Model):
    identifier = models.CharField(_("identifier"), max_length=50)
    date = models.DateField(_("date"), help_text=_("Invoice (creation) date"))
    amount = models.DecimalField(_("amount"), max_digits=6, decimal_places=2)
    pdf = PrivateMediaFileField(
        _("pdf"), blank=True, upload_to="expenses/invoices/%Y/%m"
    )
    creditor = models.ForeignKey(
        Creditor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("creditor"),
    )

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")

    def __str__(self):
        return self.identifier
