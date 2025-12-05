from django.db import models
from django.utils import timezone
from django_currentuser.db.models import CurrentUserField

from apps.common.managers import SoftDeleteManager


class AuditMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Created At", auto_now_add=True, db_index=True
    )
    created_by = CurrentUserField(
        verbose_name="Created By", related_name="%(app_label)s_%(class)s_created_by"
    )
    updated_at = models.DateTimeField(
        verbose_name="Last Updated At", auto_now=True, db_index=True
    )
    updated_by = CurrentUserField(
        verbose_name="Last Updated By",
        related_name="%(app_label)s_%(class)s_updated_by",
    )

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(
        verbose_name="Is Deleted", default=False, db_index=True
    )
    deleted_at = models.DateTimeField(verbose_name="Deleted At", null=True, blank=True)
    deleted_by = CurrentUserField(
        verbose_name="Deleted By",
        related_name="%(app_label)s_%(class)s_deleted_by",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = SoftDeleteManager()  # Returns non-deleted records only
    all_objects = models.Manager()  # Return all records including deleted ones

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])


class ActiveMixin(models.Model):
    is_active = models.BooleanField(verbose_name="Active", default=True, db_index=True)

    class Meta:
        abstract = True


class OrderingMixin(models.Model):
    order = models.PositiveIntegerField(verbose_name="Order", default=0)

    class Meta:
        abstract = True
        ordering = ["order"]


class NoteMixin(models.Model):
    notes = models.TextField(blank=True, default="", verbose_name="Notes")

    class Meta:
        abstract = True
