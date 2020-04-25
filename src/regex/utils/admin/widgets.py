from django.contrib.admin.widgets import AdminFileWidget
from django.urls import reverse
from django.utils.html import conditional_escape


class PrivateFileWidgetMixin(object):
    def __init__(self, *args, **kwargs):
        self.url_name = kwargs.pop("url_name")
        super(PrivateFileWidgetMixin, self).__init__(*args, **kwargs)

    def get_template_substitution_values(self, value):
        """
        Return value-related substitutions.
        """
        url = reverse(self.url_name, kwargs={"pk": value.instance.pk})
        return {
            "initial": conditional_escape(value),
            "initial_url": conditional_escape(url),
        }


class PrivateFileWidget(PrivateFileWidgetMixin, AdminFileWidget):
    pass
