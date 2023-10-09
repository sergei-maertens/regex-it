from django.urls import path

from .views import ExportAdministrationView

app_name = "administration"
urlpatterns = [
    path("export/", ExportAdministrationView.as_view(), name="export"),
]
