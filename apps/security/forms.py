from allauth.account.forms import AddEmailForm as AllAuthAddEmailForm
from allauth.account.forms import ChangePasswordForm as AllAuthChangePasswordForm
from allauth.account.forms import LoginForm as AllAuthLoginForm
from allauth.account.forms import ResetPasswordForm as AllAuthResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm as AllAuthResetPasswordKeyForm
from allauth.account.forms import SignupForm as AllAuthSignupForm

from apps.common.validators import username_validator
from apps.common.widgets import EmailInputWidget, PasswordInputWidget, TextInputWidget


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
