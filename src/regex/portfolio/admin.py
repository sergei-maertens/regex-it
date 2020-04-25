from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from .models import Entry


@admin.register(Entry)
class EntryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "published")
    list_filter = ("published",)
    search_fields = ("name",)
