from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^typography/$', TemplateView.as_view(template_name='typography.html')),
    url(r'^invoices/', include('regex.invoices.urls', namespace='invoices')),
    url(r'^', include('regex.homepage.urls', namespace='home')),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^admin/rosetta/', include('rosetta.urls')),
    ]
