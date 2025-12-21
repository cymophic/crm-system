from django.forms import widgets


class BaseFormWidget:
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # Common form attributes
        context["label"] = attrs.pop("label", "")
        context["help_text"] = attrs.pop("help_text", "")
        context["has_error"] = attrs.pop("has_error", False)
        context["error_message"] = attrs.pop("error_message", "")
        context["margin_class"] = attrs.pop("margin_class", "")
        context["required"] = attrs.pop("required", False)

        return context


class TextInputWidget(BaseFormWidget, widgets.TextInput):
    template_name = "forms/text_input.html"


class PasswordInputWidget(BaseFormWidget, widgets.PasswordInput):
    template_name = "forms/password_input.html"


class EmailInputWidget(BaseFormWidget, widgets.EmailInput):
    template_name = "forms/text_input.html"

    def __init__(self, attrs=None):
        default_attrs = {"type": "email"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class TextAreaWidget(BaseFormWidget, widgets.Textarea):
    template_name = "forms/text_area.html"


class SelectWidget(BaseFormWidget, widgets.Select):
    template_name = "forms/select.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # Control rendering of empty option and display label
        context["show_empty"] = attrs.pop("show_empty", True)
        context["empty_label"] = attrs.pop("empty_label", "Select Option")
        return context
