from datetime import date

from django.core.urlresolvers import reverse

from django_webtest import WebTest
from freezegun import freeze_time

from regex.crm.tests.factories import ProjectFactory
from .factories import InvoiceFactory, InvoiceItemFactory


class InvoiceViewTests(WebTest):

    @freeze_time('2015-10-21')
    def test_invoice_pdf(self):
        """
        Test that the invoice pdf is generated and downloaded.

        TODO: use X-SendFile to redirect to the private media.
        TODO: check ACL permissions
        """
        project = ProjectFactory.create(flat_fee=3500)
        invoice = InvoiceFactory.create(client=project.client, date=date(2015, 10, 15))
        InvoiceItemFactory.create(
            invoice=invoice, project=project,
            rate=3500, amount=1,
            source_object=project
        )

        self.assertFalse(invoice.invoice_number)
        invoice.generate()

        url = reverse('invoices:detail-pdf', kwargs={'invoice_number': invoice.invoice_number})
        response = self.app.get(url)
        invoice.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')
        self.assertGreater(response.content_length, 0)
        self.assertEqual(response.content_length, invoice.pdf.size)
        self.assertEqual(response.content, invoice.pdf.read())
