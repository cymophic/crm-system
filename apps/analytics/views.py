import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

logger = logging.getLogger("apps.analytics")


# Dashboard View
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        # New users go to complete profile view
        if not user.is_profile_complete:
            # Toast message
            messages.info(request, "Please complete your profile first to proceed.")

            return redirect(reverse("security:complete_profile"))
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
