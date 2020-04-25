from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel


class CompanyConfig(SingletonModel):
    company_name = models.CharField(_("company name"), max_length=255)
    company_address = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("company address"),
        default=list,
    )
    tax_identifier = models.CharField(_("tax identifier"), max_length=50)
    coc = models.CharField(_("chamber of commerce number"), max_length=100)
    iban = models.CharField(_("bank account number"), max_length=100)

    class Meta:
        verbose_name = _("company config")

    def __str__(self):
        return force_text(self._meta.verbose_name)
