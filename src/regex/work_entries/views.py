from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from regex.crm.models import Project

from .models import WorkEntry


class WorkEntryList(LoginRequiredMixin, ListView):
    model = WorkEntry
    context_object_name = 'work_entries'

    def _get_project_filters(self):
        return {
            'slug': self.kwargs['project_slug'],
            'client__contacts__user': self.request.user
        }

    def get_queryset(self):
        qs = super().get_queryset()
        filters = {'project__%s' % key: value for key, value in self._get_project_filters().items()}
        return qs.filter(**filters).annotate(duration=F('end') - F('start'))

    def get_context_data(self, **kwargs):
        qs = Project.objects.filter(**self._get_project_filters())
        kwargs['project'] = get_object_or_404(qs)
        return super().get_context_data(**kwargs)
