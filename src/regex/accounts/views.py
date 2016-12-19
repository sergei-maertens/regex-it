from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView

from regex.crm.models import Project


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.get_projects()
        return context

    def get_projects(self):
        base = Project.objects.filter(
            client__contacts__user=self.request.user
        ).select_related('client').order_by('client', 'name')
        qs = base.annotate(n_workentries=Count('workentry'))
        return qs
