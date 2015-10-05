from django.contrib import admin

from .models import WorkEntry


@admin.register(WorkEntry)
class WorkEntryAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'project', 'notes')
    list_filter = ('project__client', 'project', 'start')
    search_fields = ('notes',)
