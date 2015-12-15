from django.conf.urls import url

from .views import ContactView, HomepageView


urlpatterns = [
    url(r'^$', HomepageView.as_view(), name='home'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
]
