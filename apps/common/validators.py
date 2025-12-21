from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Allows only digits (0–9).
numeric_validator = RegexValidator(
    regex=r"^\d+$", message="Only numbers are allowed.", code="invalid_numeric"
)

# Allows only letters and numbers (A–Z, a–z, 0–9).
alphanumeric_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9]+$",
    message="Only letters and numbers are allowed.",
    code="invalid_alphanumeric",
)

# Validates URL-friendly slugs like "team-alpha-1".
slug_validator = RegexValidator(
    regex=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    message=_("Use lowercase letters, numbers, and hyphen (') only."),
    code="invalid_slug",
)

# Validates human names (letters, spaces, hyphens, apostrophes, diacritics).
human_name_validator = RegexValidator(
    regex=r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$",
    message=_("Only letters, spaces, hyphens (-), and apostrophes (') are allowed."),
    code="invalid_name",
)

# Validates usernames (3–30 chars: letters, numbers, underscore, dot, hyphen).
username_validator = RegexValidator(
    regex=r"^(?=.{3,50}$)[A-Za-z0-9._-]+$",
    message=_(
        "Must be 3 to 50 characters, using only letters, numbers, underscores (_), dots (.), or hyphens (-)."
    ),
    code="invalid_username",
)

# Validates hex colors like #fff or #ffffff.
hex_color_validator = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    message=_("Enter a valid hex color (e.g., #fff or #ffffff)."),
    code="invalid_hex_color",
)

# Validates UUIDs (versions 1–5).
uuid_validator = RegexValidator(
    regex=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
    message=_("Enter a valid UUID."),
    code="invalid_uuid",
)

# Validates business/SKU-like codes (3–32 chars, uppercase letters, numbers, _ and -).
sku_code_validator = RegexValidator(
    regex=r"^(?=.{3,32}$)[A-Z0-9_-]+$",
    message=_(
        "Must be 3 to 32 characters consisting of uppercase letters, numbers, underscores (_), and hyphens (-)."
    ),
    code="invalid_sku_code",
)


# Checks if a field value is unique in any model.
def validate_unique_field(model, field_name, value, instance=None, error_message=None):
    if not value:
        return

    query = model.objects.filter(**{field_name: value})

    if instance and instance.pk:
        query = query.exclude(pk=instance.pk)

    if query.exists():
        if error_message is None:
            error_message = f"A {model.__name__} with this {field_name} already exists."
        raise ValidationError(error_message, code=f"unique_{field_name}")


# Ensures uploaded files do not exceed the given size in megabytes.
def file_size_validator(max_mb: int):
    def _validator(f):
        if f.size > max_mb * 1024 * 1024:
            raise ValidationError(
                _(f"File too large. Maximum allowed is {max_mb} MB."),
                code="file_too_large",
            )

    return _validator


# Ensures uploaded files match one of the allowed MIME content types.
def file_content_type_validator(allowed_types: list[str]):
    def _validator(f):
        ct = getattr(f, "content_type", None)
        if ct not in allowed_types:
            raise ValidationError(
                _(f"Invalid file type. Allowed: {', '.join(allowed_types)}"),
                code="invalid_content_type",
            )

    return _validator


# Ensures a date value is not in the past.
def date_not_in_past(value: date):
    if value and value < date.today():
        raise ValidationError(_("Date cannot be in the past."), code="date_in_past")


# Ensures a date value is not in the future.
def date_not_in_future(value: date):
    if value and value > date.today():
        raise ValidationError(_("Date cannot be in the future."), code="date_in_future")


# Ensures an age (derived from birthdate) is at least the given number of years.
def age_at_least(min_years: int):
    def _validator(birthdate: date):
        if not birthdate:
            return
        today = date.today()
        age = (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )
        if age < min_years:
            raise ValidationError(
                _(f"Must be at least {min_years} years old."), code="min_age"
            )

    return _validator
