from django.views.generic import ListView

from .models import Entry


class EntryList(ListView):
    model = Entry
    queryset = Entry.objects.published()
