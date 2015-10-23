from django.conf.urls import url

from .views import InvoiceDetailView, InvoiceDetailPDFView


urlpatterns = [
    url(r'^invoice/(?P<invoice_number>\d+)/$', InvoiceDetailView.as_view(), name='detail'),
    url(r'^invoice/(?P<invoice_number>\d+)/pdf/$', InvoiceDetailPDFView.as_view(), name='detail-pdf'),
]
