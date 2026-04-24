from django.urls import reverse
from rest_framework.test import APITestCase

from cinemas.models import Cinema, Screen
from users.models import User


class CinemaTestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create_user(
            username="testadmin", password="testpass123", role="admin"
        )
        self.normal_user = User.objects.create_user(username="testuser", password="testpass123")
        self.test_cinema = Cinema.objects.create(
            name="local cinema", city="Accra", country="Ghana", total_screen=2
        )

    def test_list_cinemas_successful(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("list_create_cinema_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        results = response.data.get("results", response.data)
        self.assertTrue(len(results) > 0)

    def test_create_cinema_post_fail_for_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("list_create_cinema_view")
        data = {"name": "new cinema", "city": "Accra", "country": "Ghana", "total_screen": 2}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_create_cinema_post_success_for_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("list_create_cinema_view")
        data = {"name": "admin cinema", "city": "Accra", "country": "Ghana", "total_screen": 2}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Cinema.objects.filter(name="admin cinema").exists())

    def test_retrieve_cinema_successful(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("get_update_delete_cinema_view", args=[self.test_cinema.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ScreenTestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create_user(
            username="screenadmin", password="testpass123", role="admin"
        )
        self.normal_user = User.objects.create_user(username="screenuser", password="testpass123")
        self.cinema = Cinema.objects.create(
            name="Screen Cinema", city="Accra", country="Ghana", total_screen=2
        )
        self.screen = Screen.objects.create(
            cinema_id=self.cinema, total_seats=10, screen_number="S1"
        )

    def test_list_screens_successful(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("list_create_screen_view", args=[self.cinema.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)

    def test_create_screen_success_for_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("list_create_screen_view", args=[self.cinema.pk])
        data = {"screen_number": "S2", "total_seats": 20}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Screen.objects.filter(screen_number="S2", cinema_id=self.cinema).exists())

    def test_create_screen_fail_for_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("list_create_screen_view", args=[self.cinema.pk])
        data = {"screen_number": "S2", "total_seats": 20}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_update_screen_successful(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("get_update_delete_screen_view", args=[self.cinema.pk, self.screen.pk])
        data = {"total_seats": 50}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.screen.refresh_from_db()
        self.assertEqual(self.screen.total_seats, 50)
