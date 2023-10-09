from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest
from django.views.generic import FormView

from .forms import ExportAdministrationForm


class SuperUserRequired(UserPassesTestMixin):
    request: HttpRequest

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class ExportAdministrationView(SuperUserRequired, FormView):
    form_class = ExportAdministrationForm
    template_name = "administration/export_administration.html"
