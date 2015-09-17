from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class Contact(models.Model):

    """
    Contact details for a single contact.
    """

    label = models.CharField(_('label'), max_length=50)
    name = models.CharField(_('name'), max_length=255)
    email = models.EmailField(_('email'))
    phone = PhoneNumberField()
    address = models.CharField(_('address'), max_length=255, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True)
    city = models.CharField(_('city'), max_length=255, blank=True)
    country = CountryField(default=settings.DEFAULT_COUNTRY, verbose_name=_('Country'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __str__(self):
        return self.name


class Client(models.Model):

    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='name', unique=True)

    # global company contact details
    email = models.EmailField(_('email'))
    phone = PhoneNumberField()
    city = models.CharField(_('city'), max_length=255)
    country = CountryField(default=settings.DEFAULT_COUNTRY, verbose_name=_('Country'))

    # invoicing fields
    crn = models.CharField(_('registration number'), max_length=50, blank=True, help_text=_('KvK number'))
    vat = models.CharField(_('VAT number'), max_length=50, blank=True)

    contacts = models.ManyToManyField('Contact', blank=True)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _("client")
        verbose_name_plural = _("clients")

    def __str__(self):
        return self.name
