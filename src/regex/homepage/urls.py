from django.urls import path

from .views import ContactView, HomepageView

app_name = "home"

urlpatterns = [
    path("", HomepageView.as_view(), name="home"),
    path("contact/", ContactView.as_view(), name="contact"),
]
