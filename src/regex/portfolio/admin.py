from django.contrib import admin

from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("name", "published")
    list_filter = ("published",)
    search_fields = ("name",)
