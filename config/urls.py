from django.conf import settings
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # Admin URL
    path(settings.ADMIN_URL, admin.site.urls),
]
