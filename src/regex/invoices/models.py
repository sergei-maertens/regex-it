import logging
import re
from datetime import datetime, time, timedelta

from django.conf import settings
from django.core import validators
from django.db import models, transaction
from django.db.models import F, Sum, Max
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from regex.crm.models import TaxRates
from regex.utils.storages import private_media_storage
from regex.work_entries.models import WorkEntry


logger = logging.getLogger(__name__)


RE_INVOICE_NUMBER = re.compile(r'(?P<year>20\d{2})\d{5}$')


class Invoice(models.Model):
    client = models.ForeignKey('crm.Client')
    date = models.DateField(_('date'), help_text=_('Include work up to (including) this day.'))

    generated = models.DateTimeField(editable=False, null=True)
    invoice_number = models.CharField(
        _('invoice number'), max_length=50, blank=True,
        unique=True, default=None, null=True,
        validators=[validators.RegexValidator(RE_INVOICE_NUMBER)]
    )
    due_date = models.DateTimeField(_('due date'), null=True, blank=True)
    pdf = models.FileField(
        _('pdf'), blank=True, upload_to='invoices/%Y/%m',
        storage=private_media_storage
    )

    received = models.DateTimeField(_('received'), null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return '{client} - {date}'.format(client=self.client, date=self.date)

    def get_previous(self, **kwargs):
        kwargs['client'] = self.client
        return self.get_previous_by_date(**kwargs)

    def generate_invoice_number(self, save=True):
        """
        Invoice numbers must increment according to the Dutch legislation.

        We choose here to prefix the year that the invoice object was created,
        and number incrementingly (+1) across the years.
        """
        prefix = self.created.year
        agg = self.__class__.objects.aggregate(Max('invoice_number'))
        max_number = agg['invoice_number__max'] or '201500000'
        match = RE_INVOICE_NUMBER.match(max_number)
        if not match:
            raise ValueError('Invalid invoice number for invoice %d', self.pk)
        max_number = int(max_number[4:])
        next_number = '{:05d}'.format(max_number + 1)
        self.invoice_number = '{prefix}{number}'.format(prefix=prefix, number=next_number)
        if save:
            self.save()

    def generate(self):
        if self.generated is not None:
            return

        # collect the work entries
        try:
            previous = self.get_previous()
            lower = datetime.combine(previous.date, time(0, 0)) + timedelta(days=1)
        except self.__class__.DoesNotExist:
            previous = None
            lower = datetime(1970, 1, 1, 0, 0)
        lower = timezone.make_aware(lower)
        upper = timezone.make_aware(datetime.combine(self.date, time(23, 59, 59)))

        work_entries = WorkEntry.objects.filter(
            project__client=self.client, start__range=[lower, upper]
        ).select_related('project')

        with transaction.atomic():
            for entry in work_entries:
                InvoiceItem.objects.create(
                    invoice=self,
                    project=entry.project,
                    rate=entry.project.base_rate if not entry.project.flat_fee else 0,
                    amount=entry.delta_to_decimal(),
                    tax_rate=entry.project.tax_rate,
                    source_object=entry,
                    remarks=entry.notes
                )

            # either created from hourly rate (work_entries) or manual invoice items
            if work_entries or self.invoiceitem_set.exists():
                self.generated = timezone.now()
                self.generate_invoice_number(save=False)
                self.save()

    def regenerate(self):
        if self.received is not None:
            logger.info('Not regenerating paid invoice %d, fix this manually', self.pk)
            return

        if self.generated is not None:
            self.invoiceitem_set.all().delete()
            self.generated = None
            logger.info('Regenerating invoice %d, potentially rewriting sent-out invoices.', self.pk)
        self.generate()

    def get_totals(self):
        totals = self.invoiceitem_set.annotate(
            base=F('rate')*F('amount'),
            tax=F('rate')*F('amount')*F('tax_rate')
        ).aggregate(Sum('base'), Sum('tax'))
        return totals

    @property
    def total_no_vat(self):
        return self.get_totals()['base__sum']

    @property
    def total_vat(self):
        return self.get_totals()['tax__sum']

    @property
    def total_with_vat(self):
        totals = self.get_totals()
        return totals['base__sum'] + totals['tax__sum']

    @cached_property
    def vat_reverse_charge(self):
        return self.client.country != settings.SITE_COUNTRY


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice)
    project = models.ForeignKey('crm.Project', null=True, blank=True)

    rate = models.DecimalField(_('rate'), max_digits=10, decimal_places=2)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(
        _('tax rate'), max_digits=4, decimal_places=2,
        choices=TaxRates.choices, default=TaxRates.high
    )

    content_type = models.ForeignKey('contenttypes.ContentType', blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    source_object = GenericForeignKey()
    remarks = models.TextField(_('remarks'), blank=True)

    class Meta:
        verbose_name = _('invoice item')
        verbose_name_plural = _('invoice items')
