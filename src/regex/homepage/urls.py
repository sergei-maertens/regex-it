from django.conf.urls import url

from .views import HomepageView


urlpatterns = [
    url(r'^$', HomepageView.as_view(), name='home'),
]
