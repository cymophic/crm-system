from django.db import models


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # Return only non-deleted records
        return super().get_queryset().filter(is_deleted=False)
