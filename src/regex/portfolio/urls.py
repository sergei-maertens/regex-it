from django.conf.urls import url

from .views import EntryList


urlpatterns = [
    url(r'^$', EntryList.as_view(), name='list'),
]
