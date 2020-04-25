import os
from datetime import date

from django.test import RequestFactory, TestCase

from freezegun import freeze_time

from regex.crm.tests.factories import ProjectFactory

from ..utils import render_invoice_pdf
from .factories import InvoiceFactory, InvoiceItemFactory


class InvoiceUtilsTests(TestCase):

    @freeze_time('2015-10-21')
    def test_render_pdf(self):
        project = ProjectFactory.create(flat_fee=3500)
        invoice = InvoiceFactory.create(client=project.client, date=date(2015, 10, 15))
        InvoiceItemFactory.create(
            invoice=invoice, project=project,
            rate=3500, amount=1,
            source_object=project
        )

        self.assertFalse(invoice.invoice_number)
        invoice.generate()

        request = RequestFactory().get('/')
        render_invoice_pdf(request, invoice)

        self.assertEqual(invoice.pdf.name, 'invoices/2015/10/201500001.pdf')
        self.assertTrue(os.path.exists(invoice.pdf.path))
