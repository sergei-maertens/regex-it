from io import BytesIO

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import FileResponse, HttpRequest
from django.views.generic import FormView

from .forms import ExportAdministrationForm


class SuperUserRequired(UserPassesTestMixin):
    request: HttpRequest
    raise_exception = True

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class ExportAdministrationView(SuperUserRequired, FormView):
    form_class = ExportAdministrationForm
    template_name = "administration/export_administration.html"

    def form_valid(self, form: ExportAdministrationForm):
        export_data = form.prepare_export_date()

        response = FileResponse(
            as_attachment=True,
            filename="administration.zip",
            content_type="application/zip",
        )
        outfile = BytesIO()
        export_data.write_zip(outfile)
        outfile.seek(0)
        response.streaming_content = outfile

        return response
