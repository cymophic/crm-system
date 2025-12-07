from django.contrib.admin import SimpleListFilter


class ActiveStatusFilter(SimpleListFilter):
    title = "Active Status"
    parameter_name = "is_active"

    def lookups(self, request, model_admin):
        # Define filter options
        return (
            ("1", "Yes"),
            ("0", "No"),
        )

    def queryset(self, request, queryset):
        # Filter queryset based on selection
        if self.value() == "1":
            return queryset.filter(is_active=True)
        if self.value() == "0":
            return queryset.filter(is_active=False)


class StaffStatusFilter(SimpleListFilter):
    title = "Staff Status"
    parameter_name = "is_staff"

    def lookups(self, request, model_admin):
        # Define filter options
        return (
            ("1", "Yes"),
            ("0", "No"),
        )

    def queryset(self, request, queryset):
        # Filter queryset based on selection
        if self.value() == "1":
            return queryset.filter(is_staff=True)
        if self.value() == "0":
            return queryset.filter(is_staff=False)


class SuperuserStatusFilter(SimpleListFilter):
    title = "Superuser Status"
    parameter_name = "is_superuser"

    def lookups(self, request, model_admin):
        # Define filter options
        return (
            ("1", "Yes"),
            ("0", "No"),
        )

    def queryset(self, request, queryset):
        # Filter queryset based on selection
        if self.value() == "1":
            return queryset.filter(is_superuser=True)
        if self.value() == "0":
            return queryset.filter(is_superuser=False)
