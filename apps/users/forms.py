from django import forms
from django.urls import reverse

from apps.common.validators import username_validator
from apps.users.models import User
from apps.users.validators import validate_unique_email, validate_unique_username


class UserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply validators to fields
        if "username" in self.fields:
            self.fields["username"].validators.append(username_validator)

        if self.instance and self.instance.pk:
            if "email" in self.fields:
                url = reverse(
                    "admin:auth_user_password_change", args=[self.instance.pk]
                )
                self.fields["email"].help_text = (
                    f'You can change the password of this user using <a href="{url}" style="color: #2563eb; text-decoration: underline;">this form</a>.'
                )

        if "phone" in self.fields:
            self.fields["phone"].error_messages[
                "invalid"
            ] = "Use the local format (e.g., 09XX XXX XXXX) or include the country code (e.g., +63 XXX XXX XXXX)"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        validate_unique_email(email, self.instance)

        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        validate_unique_username(username, self.instance)

        return username

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "groups",
            "user_permissions",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
        ]
        labels = {
            "date_joined": "Date Joined",
            "last_login": "Last Login",
        }
