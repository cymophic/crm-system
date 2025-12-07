from django.contrib import admin
from django.contrib.sites.models import Site
from unfold.admin import ModelAdmin

# Unregister the default Site model admin
admin.site.unregister(Site)


# Site Model
@admin.register(Site)
class SiteAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "domain",
    )
    search_fields = (
        "id",
        "name",
        "domain",
    )
