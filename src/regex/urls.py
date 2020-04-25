from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('regex.accounts.urls')),
    url(r'^invoices/', include('regex.invoices.urls')),
    url(r'^portfolio/', include('regex.portfolio.urls')),
    url(r'^work_entries/', include('regex.work_entries.urls')),
    url(r'^', include('regex.homepage.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^typography/$', TemplateView.as_view(template_name='typography.html')),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
