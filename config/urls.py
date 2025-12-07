from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin URL
    path(settings.ADMIN_URL, admin.site.urls),
    # Allauth URLs
    path("", include("allauth.urls")),
    # Base URLs
    path("", include("apps.base.urls")),
    # Dashboard and Analytics URLs
    path("", include("apps.analytics.urls")),
    # Authentication and Security URLs
    # path("", include("apps.security.urls")),
]
