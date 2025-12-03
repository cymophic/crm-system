import logging

from django.contrib.auth.models import UserManager as BaseUserManager

logger = logging.getLogger("apps.web")


class UserManager(BaseUserManager):
    def _generate_username(self, first_name, last_name):
        # Generate unique username from first and last name
        first_clean = first_name.replace(" ", "").lower()
        last_clean = last_name.replace(" ", "").lower()
        base_username = f"{first_clean}.{last_clean}"
        username = base_username[:50]
        counter = 1

        # Handle duplicates by appending a number
        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        if username != base_username:
            logger.debug(f"Username collision resolved: {base_username} -> {username}")

        return username

    def create_user(self, email, password=None, **extra_fields):
        # Validate email
        if not email:
            raise ValueError("Email is required")

        # Auto-generate username if not provided
        if not extra_fields.get("username"):
            first_name = extra_fields.get("first_name")
            last_name = extra_fields.get("last_name")

            if first_name and last_name:
                extra_fields["username"] = self._generate_username(
                    first_name, last_name
                )

        # Create user
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Set superuser defaults
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Validate superuser fields
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)
