from django import forms

from regex.utils.admin.widgets import PrivateFileWidget

from .models import Invoice


class AdminInvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'pdf': PrivateFileWidget(url_name='admin:invoices_invoice_pdf')
        }
