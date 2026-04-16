from django.test import TestCase

from users.models import User

# Create your tests here.


class CustomUserTest(TestCase):
    def test_create_user_successfull(self):
        User.objects.create(username="test", password="password", role="user")
        is_ava = User.objects.filter(username="test").exists()

        self.assertTrue(is_ava, True)

    def test_create_default_role_successfull(self):
        User.objects.create(username="test", password="password")
        user = User.objects.get(username="test")

        self.assertTrue(user.role, "USER")

    def test_create_admin_role_successfull(self):
        User.objects.create(username="test", password="password", role="admin")
        user = User.objects.get(username="test")

        self.assertTrue(user.role, "ADMIN")
