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

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")

    def __str__(self):
        return self.identifier


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

    objects = ExpensesConfigurationManager()
