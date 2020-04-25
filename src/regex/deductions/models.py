from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _

from privates.fields import PrivateMediaFileField


class Deduction(models.Model):
    name = models.CharField(_('name'), max_length=255)
    notes = models.TextField(_('notes'), blank=True, null=True)
    receipt = PrivateMediaFileField(_('receipt'), blank=True, upload_to='receipts/%Y/%m')
    date = models.DateField(_('date'), default=date.today)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('deduction')
        verbose_name_plural = _('deductions')

    def __str__(self):
        return self.name
