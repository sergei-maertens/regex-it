from django.conf.urls import url

from .views import EntryList

app_name = "portfolio"

urlpatterns = [
    url(r'^$', EntryList.as_view(), name='list'),
]
