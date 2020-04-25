from datetime import date

from django.conf import settings
from django.urls import reverse

from django_webtest import WebTest
from freezegun import freeze_time

from regex.accounts.tests.factories import SuperUserFactory, UserFactory
from regex.crm.tests.factories import ContactFactory, ProjectFactory

from .factories import InvoiceFactory, InvoiceItemFactory


class InvoiceViewTests(WebTest):
    def setUp(self):
        super(InvoiceViewTests, self).setUp()

        self.user = UserFactory.create()
        self.superuser = SuperUserFactory.create()

    @freeze_time("2015-10-21")
    def test_invoice_pdf(self):
        """
        Test that the invoice pdf is generated and downloaded.
        """
        project = ProjectFactory.create(flat_fee=3500)
        invoice = InvoiceFactory.create(client=project.client, date=date(2015, 10, 15))
        InvoiceItemFactory.create(
            invoice=invoice, project=project, rate=3500, amount=1, source_object=project
        )

        project.client.contacts.add(ContactFactory(user=self.user))

        self.assertFalse(invoice.invoice_number)
        invoice.generate()

        url = reverse(
            "invoices:detail-pdf", kwargs={"invoice_number": invoice.invoice_number}
        )
        response = self.app.get(url)
        expected = "{}?next={}".format(settings.LOGIN_URL, url)
        self.assertRedirects(response, expected, fetch_redirect_response=False)

        response = self.app.get(url, user=self.user)
        invoice.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/pdf")
        self.assertGreater(response.content_length, 0)
        self.assertEqual(response.content_length, invoice.pdf.size)
        self.assertEqual(response.content, invoice.pdf.read())
