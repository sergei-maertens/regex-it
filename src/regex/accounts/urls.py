from django.conf.urls import url

from .views import DashboardView

app_name = "accounts"
urlpatterns = [url(r"^dashboard/$", DashboardView.as_view(), name="dashboard")]
