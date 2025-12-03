import logging
import warnings

from django.contrib.auth import get_user_model
from django.test import TestCase

# Disable all logging during tests
logging.disable(logging.CRITICAL)

# Suppress staticfiles warning during tests
warnings.filterwarnings(
    "ignore",
    message="No directory at.*staticfiles",
    category=UserWarning,
)

User = get_user_model()


class UserCreationTests(TestCase):
    # Test: Create regular user with valid data
    def test_create_user_valid(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    # Test: Create superuser with valid data
    def test_create_superuser_valid(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    # Test: Email is required
    def test_email_required(self):
        with self.assertRaises(
            ValueError, msg="Should raise ValueError when email is missing"
        ):
            User.objects.create_user(
                email="",
                password="testpass123",
            )


class UserUniquenessTests(TestCase):
    # Test: Username auto-generation from first and last name
    def test_username_auto_generation(self):
        user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            job_title="Developer",
            password="testpass123",
        )
        self.assertEqual(
            user.username,
            "john.doe",
            msg="Username should be auto-generated as 'first.last'",
        )

    # Test: Handle duplicate username
    def test_username_duplicate_handling(self):
        User.objects.create_user(
            first_name="Jane",
            last_name="Smith",
            email="jane1@example.com",
            job_title="Developer",
            password="testpass123",
        )
        user2 = User.objects.create_user(
            first_name="Jane",
            last_name="Smith",
            email="jane2@example.com",
            job_title="Manager",
            password="testpass123",
        )
        self.assertEqual(
            user2.username,
            "jane.smith1",
            msg="Duplicate usernames should append a number",
        )

    # Test: Email must be unique
    def test_email_unique(self):
        from django.db import IntegrityError

        User.objects.create_user(
            first_name="User",
            last_name="One",
            email="duplicate@example.com",
            job_title="Dev",
            password="testpass123",
        )
        with self.assertRaises(
            IntegrityError, msg="Duplicate email should raise IntegrityError"
        ):
            User.objects.create_user(
                first_name="User",
                last_name="Two",
                email="duplicate@example.com",
                job_title="Dev",
                password="testpass123",
            )


class UserStringRepresentationTests(TestCase):
    # Test: User string representation
    def test_user_str(self):
        user = User.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            job_title="Manager",
            password="testpass123",
        )
        self.assertEqual(
            str(user), "Jane Doe", msg="String representation should be full name"
        )


class UserAuthenticationTests(TestCase):
    # Test: Password is hashed, not stored as plain text
    def test_password_is_hashed(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.assertNotEqual(user.password, "testpass123")
        self.assertTrue(user.check_password("testpass123"))

    # Test: Set new password
    def test_set_password(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="oldpass123",
        )
        user.set_password("newpass123")
        user.save()
        self.assertTrue(user.check_password("newpass123"))
        self.assertFalse(user.check_password("oldpass123"))

    # Test: Check wrong password fails
    def test_check_wrong_password(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="correctpass",
        )
        self.assertFalse(user.check_password("wrongpass"))


class UserPermissionsTests(TestCase):
    # Test: Regular user has no staff permissions
    def test_regular_user_not_staff(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="pass123",
        )
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    # Test: Superuser has all permissions
    def test_superuser_has_all_perms(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )
        self.assertTrue(admin.has_perm("any.permission"))
        self.assertTrue(admin.has_module_perms("any_app"))

    # Test: Staff user without superuser has limited perms
    def test_staff_user_limited_perms(self):
        staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="pass123",
        )
        staff.is_staff = True
        staff.save()
        self.assertTrue(staff.is_staff)
        self.assertFalse(staff.has_perm("any.permission"))
