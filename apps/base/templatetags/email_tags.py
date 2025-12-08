from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_emails(email_type):
    email_settings = {
        "helpdesk": settings.EMAIL_HELPDESK,
        "admin": settings.EMAIL_ADMIN,
    }
    return ",".join(email_settings.get(email_type, []))
