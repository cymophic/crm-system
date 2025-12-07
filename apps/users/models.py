import logging

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as BaseGroup
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.mixins import OrderingMixin

from .managers import UserManager

logger = logging.getLogger("apps.users")


class Group(OrderingMixin, BaseGroup):
    class Meta:
        proxy = False
        ordering = ["order", "name"]
        verbose_name = "Group"


class User(AbstractUser):
    # Custom manager
    objects = UserManager()

    # Authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "job_title",
        "username",
    ]

    # Default field overrides
    first_name = models.CharField(verbose_name="First Name", max_length=150)
    last_name = models.CharField(verbose_name="Last Name", max_length=150)
    username = models.CharField(verbose_name="Username", max_length=50, unique=True)
    email = models.EmailField(verbose_name="Email Address", unique=True)
    groups = models.ManyToManyField(
        "users.Group",
        verbose_name="Groups",
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )

    # Custom fields
    job_title = models.CharField(verbose_name="Job Title", max_length=200)
    phone = PhoneNumberField(verbose_name="Phone Number", blank=True)

    class Meta:
        verbose_name = "User"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["first_name", "last_name"]),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Log new user
            logger.info(
                f"New user created: {self.username} "
                f"Email: {self.get_field('email')}, "
                f"Phone: {self.get_field('phone')}, "
                f"First Name: {self.get_field('first_name')}, "
                f"Last Name: {self.get_field('last_name')}, "
                f"Job Title: {self.get_field('job_title')}"
            )

    @property
    def is_profile_complete(self):
        # Check if all required profile fields are filled
        required_fields = ["first_name", "last_name", "job_title"]
        return all(
            getattr(self, field, None) not in [None, ""] for field in required_fields
        )

    # Returns formatted phone or 'N/A' if blank
    def get_field(self, field_name):
        value = getattr(self, field_name, None)
        if value is None or value == "":
            return "N/A"
        return str(value)

    def __str__(self):
        return self.get_full_name()
