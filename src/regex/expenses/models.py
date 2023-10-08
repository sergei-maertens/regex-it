import hashlib
from contextlib import nullcontext
from typing import BinaryIO

from django.db import models
from django.utils.translation import gettext_lazy as _

from privates.fields import PrivateMediaFileField
from solo.models import SingletonModel


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
    # for automatic generation -> post processing & metadata
    md5_hash = models.CharField(_("MD5 file hash"), max_length=32, blank=True)
    notes = models.TextField(_("notes"), blank=True)
    review_required = models.BooleanField(_("manual review required"), default=False)

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")

    def __str__(self):
        return self.identifier

    @staticmethod
    def calculate_hash(filelike: BinaryIO) -> str:
        return hashlib.md5(filelike.read()).hexdigest()

    def save(self, *args, **kwargs):
        cm = self.pdf.open("rb") if not self.md5_hash else nullcontext()
        with cm as file:
            if not self.md5_hash:
                assert file is not None
                self.md5_hash = self.calculate_hash(file)

            super().save(*args, **kwargs)


class ExpensesConfigurationManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related(
            "transip_creditor",
        )


class ExpensesConfiguration(SingletonModel):
    transip_creditor = models.OneToOneField(
        Creditor,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("TransIP creditor"),
    )
    tmobile_creditor = models.OneToOneField(
        Creditor,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("T-Mmobile creditor"),
    )
    kpn_creditor = models.OneToOneField(
        Creditor,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("KPN creditor"),
    )

    objects = ExpensesConfigurationManager()
