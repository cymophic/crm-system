import logging

from allauth.account.signals import user_logged_in, user_logged_out
from django.conf import settings
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

logger = logging.getLogger("apps.security")


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    # Log successful user login
    ip_address = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")

    logger.info(
        f"User logged in - Username: {user.username}, Email: {user.email}, "
        f"IP: {ip_address}, User-Agent: {user_agent}"
    )


@receiver(user_logged_out)
def log_user_logout(sender, request=None, user=None, **kwargs):
    # Log user logout
    if request and user and user.is_authenticated:
        ip_address = get_client_ip(request)
        logger.info(
            f"User logged out - Username: {user.username}, Email: {user.email}, IP: {ip_address}"
        )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    # Log failed login attempts
    ip_address = get_client_ip(request)
    username = credentials.get("username") or credentials.get("email", "Unknown")

    logger.warning(
        f"Failed login attempt - Username/Email: {username}, IP: {ip_address}"
    )


def get_client_ip(request):
    # Get client IP address from request
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
