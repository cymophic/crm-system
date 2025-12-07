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
    pass
