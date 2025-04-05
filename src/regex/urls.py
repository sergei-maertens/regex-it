from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from maykin_2fa import monkeypatch_admin
from maykin_2fa.urls import urlpatterns, webauthn_urlpatterns

from regex.invoices.dev_views import InvoicePDFTestView

monkeypatch_admin()

urlpatterns = [
    path("admin/", include((urlpatterns, "maykin_2fa"))),
    path("admin/", include((webauthn_urlpatterns, "two_factor"))),
    path("admin/", admin.site.urls),
    path("administration/", include("regex.administration.urls")),
    path("portfolio/", include("regex.portfolio.urls")),
    path("_monitoring/", include("regex.monitoring.urls")),
    path("", include("regex.homepage.urls")),
]

# NOTE: The staticfiles_urlpatterns also discovers static files (ie. no need to run collectstatic). Both the static
# folder and the media folder are only served via Django if DEBUG = True.
urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True
)

if settings.DEBUG and apps.is_installed("debug_toolbar"):
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += [
        path(
            "dev/invoices/<int:pk>/pdf/",
            InvoicePDFTestView.as_view(),
            name="dev-invoice-pdf",
        ),
    ]
