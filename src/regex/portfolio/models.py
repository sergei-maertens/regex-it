from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField


class Entry(models.Model):

    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='name', unique=True)
    image = models.ImageField(_('image'), blank=True)

    description = models.TextField(_('description'), blank=True)

    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(_('published'), default=False)

    class Meta:
        verbose_name = _('portfolio entry')
        verbose_name_plural = _('portfolio entries')
        ordering = ['order']

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return
