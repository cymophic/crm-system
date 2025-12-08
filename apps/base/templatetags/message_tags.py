from django import template

register = template.Library()

MESSAGE_CLASSES = {
    "error": "bg-(--input-bg-error) border border-(--alert-error-border) text-(--alert-error-text)",
    "danger": "bg-(--input-bg-error) border border-(--alert-error-border) text-(--alert-error-text)",
    "warning": "bg-(--alert-warning-bg) border border-(--alert-warning-border) text-(--alert-warning-text)",
    "success": "bg-(--alert-success-bg) border border-(--alert-success-border) text-(--alert-success-text)",
    "info": "bg-(--alert-info-bg) border border-(--alert-info-border) text-(--alert-info-text)",
    "default": "bg-(--alert-default-bg) border border-(--alert-default-border) text-(--alert-default-text)",
}

CLOSE_BUTTON_CLASSES = {
    "error": "text-(--alert-error-icon) hover:text-(--text-error)",
    "danger": "text-(--alert-error-icon) hover:text-(--text-error)",
    "warning": "text-(--alert-warning-icon) hover:text-(--alert-warning-icon)",
    "success": "text-(--alert-success-icon) hover:text-(--alert-success-icon)",
    "info": "text-(--alert-info-icon) hover:text-(--alert-info-icon)",
    "default": "text-(--text-muted) hover:text-(--text-body)",
}


@register.filter
def message_classes(tag):
    return MESSAGE_CLASSES.get(tag, MESSAGE_CLASSES["default"])


@register.filter
def close_button_classes(tag):
    return CLOSE_BUTTON_CLASSES.get(tag, CLOSE_BUTTON_CLASSES["default"])
