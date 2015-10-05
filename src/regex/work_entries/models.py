from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from dateutil.relativedelta import relativedelta


class WorkEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey('crm.Project')
    start = models.DateTimeField(_('start'))
    end = models.DateTimeField(_('end'))

    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = _('work entry')
        verbose_name_plural = _('work entries')
        ordering = ('-start',)

    # TODO: date validation...

    def __str__(self):
        return '{project} - {start} - {end}'.format(
            project=self.project, start=self.start, end=self.end
        )

    def delta_to_decimal(self, round=False):
        """
        Convert end - start to a decimal expressing the amount of hours spent.

        Durations are optionally rounded to the nearest quarter.
        """
        timedelta = self.end - self.start
        delta = relativedelta(seconds=timedelta.total_seconds())

        total_minutes = delta.days*24*60 + delta.hours * 60 + delta.minutes + delta.seconds / 60
        if round:
            remainder = total_minutes % 15
            if remainder > 7.5:
                total_minutes += (15 - remainder)
            else:
                total_minutes -= remainder
        total_hours = total_minutes * 60
        return Decimal(str(total_hours))
