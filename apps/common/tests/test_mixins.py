import logging
import warnings

from django.contrib.auth import get_user_model
from django.db import connection, models
from django.test import TransactionTestCase

from apps.common.mixins import (
    ActiveMixin,
    AuditMixin,
    NoteMixin,
    OrderingMixin,
    SoftDeleteMixin,
)

User = get_user_model()

# Disable all logging during tests
logging.disable(logging.CRITICAL)


# Suppress staticfiles warning during tests
warnings.filterwarnings(
    "ignore",
    message="No directory at.*staticfiles",
    category=UserWarning,
)

# ------------------------------------
# Test Models
# ------------------------------------


class TestAuditModel(AuditMixin):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "common"


class TestSoftDeleteModel(SoftDeleteMixin):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "common"


class TestActiveModel(ActiveMixin):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "common"


class TestOrderingModel(OrderingMixin):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "common"
        ordering = ["order"]


class TestNoteModel(NoteMixin):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "common"


# ------------------------------------
# Test Cases
# ------------------------------------


class AuditMixinTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestAuditModel)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(TestAuditModel)

    # Test: Audit fields auto-populate on creation
    def test_audit_fields_on_create(self):
        obj = TestAuditModel.objects.create(name="Test")
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)

    # Test: updated_at changes on save
    def test_updated_at_changes(self):
        obj = TestAuditModel.objects.create(name="Test")
        old_updated = obj.updated_at
        obj.name = "Updated"
        obj.save()
        self.assertGreater(obj.updated_at, old_updated)


class SoftDeleteMixinTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestSoftDeleteModel)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(TestSoftDeleteModel)

    # Test: soft_delete sets flags correctly
    def test_soft_delete(self):
        obj = TestSoftDeleteModel.objects.create(name="Test")
        obj.soft_delete()
        self.assertTrue(obj.is_deleted)
        self.assertIsNotNone(obj.deleted_at)

    # Test: restore clears deletion flags
    def test_restore(self):
        obj = TestSoftDeleteModel.objects.create(name="Test")
        obj.soft_delete()
        obj.restore()
        self.assertFalse(obj.is_deleted)
        self.assertIsNone(obj.deleted_at)
        self.assertIsNone(obj.deleted_by)

    # Test: objects manager excludes deleted records
    def test_objects_excludes_deleted(self):
        active = TestSoftDeleteModel.objects.create(name="Active")
        deleted = TestSoftDeleteModel.objects.create(name="Deleted")
        deleted.soft_delete()

        # objects should only return non-deleted
        queryset = TestSoftDeleteModel.objects.all()
        self.assertEqual(queryset.count(), 1)
        self.assertIn(active, queryset)
        self.assertNotIn(deleted, queryset)

    # Test: all_objects includes deleted records
    def test_all_objects_includes_deleted(self):
        active = TestSoftDeleteModel.objects.create(name="Active")
        deleted = TestSoftDeleteModel.objects.create(name="Deleted")
        deleted.soft_delete()

        # all_objects should return everything
        queryset = TestSoftDeleteModel.all_objects.all()
        self.assertEqual(queryset.count(), 2)
        self.assertIn(active, queryset)
        self.assertIn(deleted, queryset)


class ActiveMixinTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestActiveModel)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(TestActiveModel)

    # Test: is_active defaults to True
    def test_is_active_default(self):
        obj = TestActiveModel.objects.create(name="Test")
        self.assertTrue(obj.is_active)


class OrderingMixinTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestOrderingModel)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(TestOrderingModel)

    # Test: order defaults to 0
    def test_order_default(self):
        obj = TestOrderingModel.objects.create(name="Test")
        self.assertEqual(obj.order, 0)

    # Test: objects sort by order field
    def test_ordering(self):
        TestOrderingModel.objects.create(name="Third", order=3)
        TestOrderingModel.objects.create(name="First", order=1)
        TestOrderingModel.objects.create(name="Second", order=2)

        ordered = list(TestOrderingModel.objects.all())
        self.assertEqual(ordered[0].name, "First")
        self.assertEqual(ordered[1].name, "Second")
        self.assertEqual(ordered[2].name, "Third")


class NoteMixinTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestNoteModel)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(TestNoteModel)

    # Test: notes defaults to empty string
    def test_notes_default(self):
        obj = TestNoteModel.objects.create(name="Test")
        self.assertEqual(obj.notes, "")
