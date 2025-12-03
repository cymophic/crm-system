from apps.common.validators import validate_unique_field
from apps.users.models import User


# Validates that email is unique
def validate_unique_email(email, instance=None):
    validate_unique_field(
        model=User,
        field_name="email",
        value=email,
        instance=instance,
        error_message="This email address is already registered.",
    )


# Validates that employee_id is unique
def validate_unique_employee_id(employee_id, instance=None):
    validate_unique_field(
        model=User,
        field_name="employee_id",
        value=employee_id,
        instance=instance,
        error_message="This employee ID is already in use.",
    )


# Validates that username is unique
def validate_unique_username(username, instance=None):
    validate_unique_field(
        model=User,
        field_name="username",
        value=username,
        instance=instance,
        error_message="A user with this username already exists.",
    )
