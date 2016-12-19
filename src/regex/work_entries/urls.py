from django.conf.urls import url

from .views import WorkEntryList

app_name = 'work_entries'
urlpatterns = [
    url(r'^(?P<project_slug>[\w-]+)/log/', WorkEntryList.as_view(), name='list'),
]
