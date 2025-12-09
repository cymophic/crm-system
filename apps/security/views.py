import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from apps.users.models import User

from .forms import CompleteProfileForm, EditProfileForm

logger = logging.getLogger("apps.security")


# Complete Profile View
class CompleteProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CompleteProfileForm
    template_name = "account/complete_profile.html"
    success_url = reverse_lazy("base:index")

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        # If profile is already complete, redirect to dashboard
        user = request.user
        if user.is_profile_complete:
            messages.info(request, "Your profile is already complete.")
            return redirect(reverse("analytics:dashboard"))
        else:
            # Toast message
            messages.info(request, "Please complete your profile to continue.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()

        # Log profile completion
        logger.info(
            f"Profile completed for user: {user.username} "
            f"(Employee ID: {user.get_field('employee_id')}, "
            f"Email: {user.get_field('email')}, "
            f"Phone: {user.get_field('phone')}, "
            f"First Name: {user.get_field('first_name')}, "
            f"Last Name: {user.get_field('last_name')}, "
            f"Job Title: {user.get_field('job_title')}, "
            f"Team: {user.get_field('team')})"
        )

        # Toast message
        messages.success(self.request, "Your profile has been completed successfully!")

        # Skip OTP verification on profile completion
        self.request.session["otp_verified"] = True

        return super().form_valid(form)


# Edit Profile View
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "account/edit_profile.html"
    success_url = reverse_lazy("security:edit_profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        user = form.save()

        # Log profile update
        logger.info(f"Profile updated for user: {user.username}")

        # Toast message
        messages.success(self.request, "Your profile has been updated successfully!")

        return super().form_valid(form)
