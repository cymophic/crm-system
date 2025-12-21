import logging

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import RedirectView

logger = logging.getLogger("apps.base")


# Landing View - Redirects based on authentication
class IndexView(RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user

            if not user.is_profile_complete:
                # New users go to complete profile view
                return redirect(reverse("security:complete_profile"))
            else:
                # Redirect to dashboard if profile is complete
                return redirect(reverse("analytics:dashboard"))

        # First-time visitors go to signup
        if not request.COOKIES.get("returning_user"):
            response = redirect(reverse("account_signup"))
            response.set_cookie("returning_user", "1", max_age=31536000)  # 1 year
            return response

        # Returning visitors go to login
        return redirect(reverse("account_login"))
