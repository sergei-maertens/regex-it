from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from .models import WorkEntry


@admin.register(WorkEntry)
class WorkEntryAdmin(ImportExportActionModelAdmin):
    list_display = ('start', 'end', 'project', 'notes')
    list_filter = ('project__client', 'project', 'start')
    search_fields = ('notes',)
