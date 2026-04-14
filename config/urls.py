# ./config/urls.py
# This module defines the URL routing for the Django project.


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

####### API ROUTES #######
api_patterns = [
    # OpenAPI / Swagger / ReDoc
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # urls
    path("auth/", include("apps.auth.urls", namespace="app_auth")),
    path("planner/", include("apps.planner.urls", namespace="app_planner")),
]

####### URLS #######
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_patterns))
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = (
        [path("__debug__/", include(debug_toolbar.urls))]
        + urlpatterns
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
