from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^typography/$', TemplateView.as_view(template_name='typography.html')),
    url(r'^invoices/', include('regex.invoices.urls', namespace='invoices')),
    url(r'^portfolio/', include('regex.portfolio.urls', namespace='portfolio')),
    url(r'^', include('regex.homepage.urls', namespace='home')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^admin/rosetta/', include('rosetta.urls')),
    ]
