from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _

from regex.utils.storages import private_media_storage


class Deduction(models.Model):
    name = models.CharField(_('name'), max_length=255)
    notes = models.TextField(_('notes'), blank=True, null=True)
    receipt = models.FileField(_('receipt'), blank=True, upload_to='receipts/%Y/%m', storage=private_media_storage)
    date = models.DateField(_('date'), default=date.today)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('deduction')
        verbose_name_plural = _('deductions')
