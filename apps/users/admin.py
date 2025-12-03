from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserCreationForm

from apps.users.forms import UserAdminForm
from apps.users.models import User

# List of built-in models for unregistration
MODELS = [
    Group,
]

# Unregister all models listed
for model in MODELS:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

# Group Model
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]
    list_display = ["name"]

# User Model
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserAdminForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    search_fields = ["username", "email", "first_name", "last_name"]
    readonly_fields = ["date_joined", "last_login"]
    ordering = ["-date_joined"]
    list_filter = ["is_staff", "is_superuser", "is_active", "groups"]
    list_display = ["full_name", "username", "job_title", "date_joined"]
    fieldsets = (
        ("Account", {"fields": ("email", "username")}),
        (
            "Profile",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "job_title",
                    "phone",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "job_title",
                    "phone",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
    )

    @admin.display(description="Full name", empty_value="-")
    def full_name(self, obj):
        # Returns the user's full name
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name if name else None

