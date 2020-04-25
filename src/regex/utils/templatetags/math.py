from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.filter
def percentage(value):
    """
    Format value (which is a number) as percentage.
    """
    return _('{value} %').format(value=100*value)
