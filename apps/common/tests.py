import logging
import warnings
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import connection, models
from django.test import TestCase, TransactionTestCase

from apps.common.mixins import (
    ActiveMixin,
    AuditMixin,
    NoteMixin,
    OrderingMixin,
    SoftDeleteMixin,
)
from apps.common.validators import (
    age_at_least,
    date_not_in_future,
    date_not_in_past,
    file_content_type_validator,
    file_size_validator,
    hex_color_validator,
    human_name_validator,
    sku_code_validator,
    slug_validator,
    username_validator,
    uuid_validator,
    validate_unique_field,
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


class TestUniqueModel(models.Model):
    email = models.EmailField(unique=True)

    class Meta:
        app_label = "common"


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


class UniqueFieldValidatorTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestUniqueModel)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(TestUniqueModel)

    # Test: accepts unique value
    def test_validate_unique_field_accepts_unique(self):
        TestUniqueModel.objects.create(email="test@example.com")
        # Should not raise
        validate_unique_field(TestUniqueModel, "email", "new@example.com")

    # Test: rejects duplicate value
    def test_validate_unique_field_rejects_duplicate(self):
        TestUniqueModel.objects.create(email="test@example.com")
        with self.assertRaises(ValidationError):
            validate_unique_field(TestUniqueModel, "email", "test@example.com")

    # Test: allows same value for existing instance
    def test_validate_unique_field_allows_same_for_instance(self):
        obj = TestUniqueModel.objects.create(email="test@example.com")
        # Should not raise when checking the same instance
        validate_unique_field(
            TestUniqueModel, "email", "test@example.com", instance=obj
        )


class RegexValidatorTests(TestCase):
    # Test: Accept valid slug
    def test_slug_valid(self):
        slug_validator("team-alpha-1")  # no exception

    # Test: Reject invalid slug (uppercase and punctuation)
    def test_slug_invalid(self):
        with self.assertRaises(
            ValidationError, msg="Invalid slug should raise ValidationError"
        ):
            slug_validator("Team Alpha!")

    # Test: Accept valid human name
    def test_human_name_valid(self):
        human_name_validator("María-José D'Arte")

    # Test: Reject invalid human name (digits)
    def test_human_name_invalid(self):
        with self.assertRaises(
            ValidationError, msg="Digits should be rejected in human names"
        ):
            human_name_validator("John Doe 2")

    # Test: Username length boundaries
    def test_username_bounds(self):
        username_validator("abc")
        with self.assertRaises(
            ValidationError, msg="Too-short username should be rejected"
        ):
            username_validator("ab")

    # Test: Username allowed characters
    def test_username_chars(self):
        username_validator("john.doe_123")
        with self.assertRaises(
            ValidationError, msg="Spaces should be rejected in username"
        ):
            username_validator("john doe")

    # Test: Hex color valid formats
    def test_hex_color_valid(self):
        hex_color_validator("#fff")
        hex_color_validator("#ffffff")

    # Test: Hex color invalid formats
    def test_hex_color_invalid(self):
        with self.assertRaises(ValidationError, msg="Missing # should be rejected"):
            hex_color_validator("ffffff")
        with self.assertRaises(
            ValidationError, msg="5/7-length hex should be rejected"
        ):
            hex_color_validator("#fffff")

    # Test: UUID valid
    def test_uuid_valid(self):
        uuid_validator("123e4567-e89b-12d3-a456-426614174000")

    # Test: UUID invalid
    def test_uuid_invalid(self):
        with self.assertRaises(
            ValidationError, msg="Non-UUID string should be rejected"
        ):
            uuid_validator("not-a-uuid")

    # Test: SKU valid (uppercase only)
    def test_sku_valid(self):
        sku_code_validator("SKU_001")

    # Test: SKU invalid (lowercase not allowed)
    def test_sku_invalid(self):
        with self.assertRaises(
            ValidationError, msg="Lowercase should be rejected in SKU"
        ):
            sku_code_validator("sku-001")


class FileValidatorTests(TestCase):
    # Setup: Simple file-like object
    class DummyFile:
        def __init__(self, size, content_type):
            self.size = size
            self.content_type = content_type

    # Test: File size within limit
    def test_file_size_within_limit(self):
        validate = file_size_validator(5)  # 5 MB
        validate(self.DummyFile(5 * 1024 * 1024, "image/png"))

    # Test: File size exceeds limit
    def test_file_size_exceeds_limit(self):
        validate = file_size_validator(5)  # 5 MB
        with self.assertRaises(
            ValidationError, msg="File exceeding limit should be rejected"
        ):
            validate(self.DummyFile(6 * 1024 * 1024, "image/png"))

    # Test: Allowed content type
    def test_file_content_type_allowed(self):
        validate = file_content_type_validator(["image/png", "image/jpeg"])
        validate(self.DummyFile(0, "image/png"))

    # Test: Disallowed content type
    def test_file_content_type_disallowed(self):
        validate = file_content_type_validator(["image/png", "image/jpeg"])
        with self.assertRaises(
            ValidationError, msg="Disallowed MIME type should be rejected"
        ):
            validate(self.DummyFile(0, "application/pdf"))


class DateValidatorTests(TestCase):
    # Test: Date not in past passes for today
    def test_date_not_in_past_today(self):
        date_not_in_past(date.today())

    # Test: Date not in past fails for yesterday
    def test_date_not_in_past_yesterday(self):
        with self.assertRaises(ValidationError, msg="Past date should be rejected"):
            date_not_in_past(date.today() - timedelta(days=1))

    # Test: Date not in future passes for today
    def test_date_not_in_future_today(self):
        date_not_in_future(date.today())

    # Test: Date not in future fails for tomorrow
    def test_date_not_in_future_tomorrow(self):
        with self.assertRaises(ValidationError, msg="Future date should be rejected"):
            date_not_in_future(date.today() + timedelta(days=1))

    # Test: Age validator accepts exactly at threshold
    def test_age_at_least_exact_threshold(self):
        validate_18 = age_at_least(18)
        bday = date.today().replace(year=date.today().year - 18)
        validate_18(bday)

    # Test: Age validator rejects just below threshold
    def test_age_at_least_below_threshold(self):
        validate_18 = age_at_least(18)
        bday = date.today().replace(year=date.today().year - 17)
        with self.assertRaises(
            ValidationError, msg="Underage birthdate should be rejected"
        ):
            validate_18(bday)
