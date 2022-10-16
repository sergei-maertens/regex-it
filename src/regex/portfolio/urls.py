from django.urls import path

from .views import EntryList

app_name = "portfolio"

urlpatterns = [
    path("", EntryList.as_view(), name="list"),
]
