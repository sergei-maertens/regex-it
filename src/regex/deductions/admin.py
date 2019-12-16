from django.contrib import admin
from django.db.models import Sum

from privates.admin import PrivateMediaMixin
from regex.utils.views.private_media import PrivateMediaView

from .models import Deduction


class DeductionPrivateMediaView(PrivateMediaView):
    model = Deduction
    permission_required = 'invoices.can_view_invoice'
    file_field = 'receipt'


@admin.register(Deduction)
class DeductionAdmin(PrivateMediaMixin, admin.ModelAdmin):
    list_display = ('name', 'date', 'amount')
    search_fields = ('name', 'notes')
    change_list_template = 'admin/deductions/deduction/change_list.html'
    private_media_fields = ('receipt',)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=None)

        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                queryset = cl.get_queryset(request)
                amount = queryset.aggregate(Sum('amount'))['amount__sum']
                response.context_data['total_amount'] = amount
        return response
