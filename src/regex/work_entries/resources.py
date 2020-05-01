from import_export import resources

from .models import WorkEntry


class WorkEntryResource(resources.ModelResource):
    class Meta:
        model = WorkEntry
        fields = ("user", "project", "start", "end", "notes")
