from allauth.account.forms import AddEmailForm as AllAuthAddEmailForm
from allauth.account.forms import ChangePasswordForm as AllAuthChangePasswordForm
from allauth.account.forms import LoginForm as AllAuthLoginForm
from allauth.account.forms import ResetPasswordForm as AllAuthResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm as AllAuthResetPasswordKeyForm
from allauth.account.forms import SignupForm as AllAuthSignupForm
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.common.validators import human_name_validator, username_validator
from apps.common.widgets import EmailInputWidget, PasswordInputWidget, TextInputWidget
from apps.users.models import User
from apps.users.validators import validate_unique_username


class LoginForm(AllAuthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].label = "Email"
        self.fields["login"].widget = EmailInputWidget()
        self.fields["password"].label = "Password"
        self.fields["password"].widget = PasswordInputWidget()


class SignupForm(AllAuthSignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = "Email"
        self.fields["email"].widget = EmailInputWidget(attrs={"autocomplete": "email"})

        self.fields["username"].label = "Username"
        self.fields["username"].widget = TextInputWidget(
            attrs={"autocomplete": "username"}
        )
        self.fields["username"].validators.append(username_validator)

        self.fields["password1"].label = "Password"
        self.fields["password1"].widget = PasswordInputWidget(
            attrs={"autocomplete": "new-password"}
        )

        self.fields["password2"].label = "Confirm Password"
        self.fields["password2"].widget = PasswordInputWidget(
            attrs={"autocomplete": "new-password"}
        )


class ChangePasswordForm(AllAuthChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["oldpassword"].label = "Current Password"
        self.fields["oldpassword"].widget = PasswordInputWidget()
        self.fields["password1"].label = "New Password"
        self.fields["password1"].widget = PasswordInputWidget()
        self.fields["password2"].label = "Confirm New Password"
        self.fields["password2"].widget = PasswordInputWidget()


class ResetPasswordForm(AllAuthResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email Address"
        self.fields["email"].widget = EmailInputWidget(
            attrs={"placeholder": "Enter your email address"}
        )


class ResetPasswordKeyForm(AllAuthResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "New Password"
        self.fields["password1"].widget = PasswordInputWidget()
        self.fields["password2"].label = "Confirm New Password"
        self.fields["password2"].widget = PasswordInputWidget()


class AddEmailForm(AllAuthAddEmailForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Add Email Address"
        self.fields["email"].widget = EmailInputWidget(
            attrs={
                "placeholder": "Enter new email address",
            }
        )


class CompleteProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # First Name
        self.fields["first_name"].label = "First Name"
        self.fields["first_name"].validators.append(human_name_validator)
        self.fields["first_name"].widget = TextInputWidget()

        # Last Name
        self.fields["last_name"].label = "Last Name"
        self.fields["last_name"].validators.append(human_name_validator)
        self.fields["last_name"].widget = TextInputWidget()

        # Job Title
        self.fields["job_title"].label = "Job Title"
        self.fields["job_title"].widget = TextInputWidget()

        # Phone
        self.fields["phone"].label = "Phone Number"
        self.fields["phone"].widget = TextInputWidget()
        self.fields["phone"].error_messages["invalid"] = "Enter a valid phone number"

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "job_title",
            "phone",
        ]


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Email (Read-only)
        self.fields["email"].label = "Primary Email"
        self.fields["email"].disabled = True
        email_url = reverse("account_email")
        self.fields["email"].help_text = mark_safe(
            f'Change your primary email <a href="{email_url}" class="hover:underline text-(--text-link-muted)">here</a>'
        )
        self.fields["email"].widget = EmailInputWidget()

        # Username
        self.fields["username"].label = "Username"
        self.fields["username"].validators.append(username_validator)
        self.fields["username"].widget = TextInputWidget()

        # First Name
        self.fields["first_name"].label = "First Name"
        self.fields["first_name"].validators.append(human_name_validator)
        self.fields["first_name"].widget = TextInputWidget()

        # Last Name
        self.fields["last_name"].label = "Last Name"
        self.fields["last_name"].validators.append(human_name_validator)
        self.fields["last_name"].widget = TextInputWidget()

        # Job Title
        self.fields["job_title"].label = "Job Title"
        self.fields["job_title"].widget = TextInputWidget()

        # Phone
        self.fields["phone"].label = "Phone Number"
        self.fields["phone"].widget = TextInputWidget()
        self.fields["phone"].error_messages["invalid"] = "Enter a valid phone number"

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
            "job_title",
            "phone",
            "email",
        ]
