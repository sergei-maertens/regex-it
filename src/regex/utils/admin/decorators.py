from functools import wraps

from django.core.urlresolvers import reverse


def get_urlname(obj):
    app_label, model_name = obj._meta.app_label, obj._meta.model_name
    return u'admin:{}_{}_change'.format(app_label, model_name)


def link_list(urlname=None, short_description=None):
    """
    Decorates a modeladmin method to display a list of related links.

    :param urlname: optional, by default it will take the related objects change url
    :param short_description: text to use as column header, optional

    Usage:

    >>> class MyAdmin(admin.ModelAdmin):
            list_display = ('related_objects',)

            @link_list('admin:myapp_relatedobject_change', short_description='my related objects')
            def related_objects(self, obj):
                return obj.relatedobject_set.all()

    The ModelAdmin method then returns a comma-separated list of clickable links.
    """
    def decorator(method):
        method.allow_tags = True
        if short_description:
            method.short_description = short_description

        @wraps(method)
        def f(*args, **kwargs):
            related_qs = method(*args, **kwargs)
            return u', '.join(
                    [u'<a href="{}">{}</a>'.format(
                        reverse(urlname or get_urlname(rel), args=[rel.pk]),
                        rel
                    ) for rel in related_qs])
        return f
    return decorator
