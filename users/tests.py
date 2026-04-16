from django.test import TestCase

from users.models import User

# Create your tests here.


class CustomUserTest(TestCase):
    def test_create_user_successfull(self):
        User.objects.create(username="test", password="password")
        is_ava = User.objects.filter(username="test").exists()

        self.assertTrue(is_ava, True)
