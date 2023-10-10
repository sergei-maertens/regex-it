import zipfile
from datetime import date
from io import BytesIO
from pathlib import Path

from django.test import TestCase
from django.urls import reverse

from django_webtest import WebTest
from privates.test import temp_private_root

from regex.accounts.tests.factories import SuperUserFactory, UserFactory
from regex.expenses.tests.factories import InvoiceFactory as DebitInvoiceFactory
from regex.invoices.tests.factories import InvoiceFactory as CreditInvoiceFactory


class AccessControlTests(TestCase):
    def test_must_be_superuser(self):
        users = (
            None,
            UserFactory.create(is_staff=False, is_superuser=False),
            UserFactory.create(is_staff=True, is_superuser=False),
        )
        url = reverse("administration:export")

        for user in users:
            with self.subTest(
                user=user,
                is_staff=user.is_staff if user else False,
                is_superuser=user.is_superuser if user else False,
            ):
                self.client.force_login(user) if user else None

                response = self.client.get(url)

                self.assertEqual(response.status_code, 403)

    def test_as_superuser(self):
        url = reverse("administration:export")
        user = SuperUserFactory.create()
        self.client.force_login(user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class ExportTests(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user = SuperUserFactory.create()

    def test_export_form_validation_no_date_given(self):
        url = reverse("administration:export")
        export_page = self.app.get(url, user=self.user)
        form = export_page.form

        form["quarter"].select("")
        response = form.submit()

        self.assertEqual(response.status_code, 200)  # validation errors
        self.assertFalse(response.context["form"].is_valid())

    def test_empty_export_current_quarter(self):
        url = reverse("administration:export")
        export_page = self.app.get(url, user=self.user)
        form = export_page.form

        form["quarter"].select("current")
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(int(response["Content-Length"]), 0)
        self.assertEqual(response["Content-Type"], "application/zip")

    def test_empty_export_previous_quarter(self):
        url = reverse("administration:export")
        export_page = self.app.get(url, user=self.user)
        form = export_page.form

        form["quarter"].select("previous")
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(int(response["Content-Length"]), 0)
        self.assertEqual(response["Content-Type"], "application/zip")

    def test_empty_explicit_start_end_dates(self):
        url = reverse("administration:export")
        export_page = self.app.get(url, user=self.user)
        form = export_page.form

        form["quarter"].select("")
        form["start"] = "2023-01-01"
        form["end"] = "2023-12-31"
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(int(response["Content-Length"]), 0)
        self.assertEqual(response["Content-Type"], "application/zip")

    @temp_private_root()
    def test_actual_pdfs_exported(self):
        url = reverse("administration:export")
        export_page = self.app.get(url, user=self.user)
        form = export_page.form
        invoice1 = CreditInvoiceFactory.create(with_pdf=True, date=date(2022, 3, 14))
        invoice2 = CreditInvoiceFactory.create(with_pdf=True, date=date(2023, 10, 10))
        assert invoice1.pdf.storage.exists(invoice1.pdf.name)
        assert invoice2.pdf.storage.exists(invoice2.pdf.name)
        invoice3 = DebitInvoiceFactory.create(with_pdf=True, date=date(2022, 12, 31))
        invoice4 = DebitInvoiceFactory.create(with_pdf=True, date=date(2023, 1, 1))

        form["quarter"].select("")
        form["start"] = "2023-01-01"
        form["end"] = "2023-12-31"
        response = form.submit()

        self.assertEqual(response.status_code, 200)

        with zipfile.ZipFile(BytesIO(response.content)) as zf:
            names = zf.namelist()

        self.assertIn("credit/", names)
        self.assertNotIn(f"credit/{Path(invoice1.pdf.name).name}", names)
        self.assertIn(f"credit/{Path(invoice2.pdf.name).name}", names)

        self.assertIn("debit/", names)
        self.assertNotIn(f"debit/{Path(invoice3.pdf.name).name}", names)
        self.assertIn(f"debit/{Path(invoice4.pdf.name).name}", names)
