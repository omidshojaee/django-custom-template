from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.


User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='super@user.com', password='foo'
        )
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False
            )

    def test_email_normalize(self):
        email = 'TEST@EXAMPLE.COM'
        user = User.objects.create_user(email=email, password='foo')
        self.assertEqual(user.email, 'TEST@example.com')


class UserModelTests(TestCase):
    def test_user_creation(self):
        User.objects.create_user(email='test@example.com', password='foo')
        self.assertEqual(User.objects.count(), 1)

    def test_email_is_unique(self):
        User.objects.create_user(email='test@example.com', password='foo')
        with self.assertRaises(Exception):  # Could be IntegrityError or ValidationError
            User.objects.create_user(email='test@example.com', password='bar')

    def test_email_max_length(self):
        long_email = 'a' * 245 + '@example.com'  # 255 characters
        with self.assertRaises(ValidationError):
            user = User(email=long_email, password='foo')
            user.full_clean()

    def test_last_login_null(self):
        user = User.objects.create_user(email='test@example.com', password='foo')
        self.assertIsNone(user.last_login)

    def test_user_str_method(self):
        user = User.objects.create_user(email='test@example.com', password='foo')
        self.assertEqual(str(user), 'test@example.com')

    def test_user_get_full_name(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='foo',
            first_name='Test',
            last_name='User',
        )
        self.assertEqual(user.get_full_name(), 'Test User')

    def test_user_get_short_name(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='foo',
            first_name='Test',
            last_name='User',
        )
        self.assertEqual(user.get_short_name(), 'Test')
