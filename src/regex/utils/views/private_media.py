from django.views.generic import DetailView

from rules.contrib.views import PermissionRequiredMixin
from sendfile import sendfile


class PrivateMediaView(PermissionRequiredMixin, DetailView):

    """
    View that requires a permission to match to view a file.
    """
    file_field = None

    def get(self, request, *args, **kwargs):
        filename = getattr(self.get_object(), self.file_field).path
        return sendfile(request, filename)
