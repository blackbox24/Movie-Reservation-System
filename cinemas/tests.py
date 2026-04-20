# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase

from cinemas.models import Cinema, Screen
from users.models import User

# class MovieTest(APITestCase):
#     def setUp(self) -> None:
#         self.admin_user = User.objects.create_user(
#             username="testadmin", password="testpass123", role="admin"
#         )
#         self.normal_user = User.objects.create_user(username="test1admin", password="testpass123")
#         self.test_cinema = Cinema.objects.create(
#             name="local cinema", city="Accra", country="Ghana", total_screen=2
#         )

#     def test_create_cinema_successful(self):
#         self.client.force_authenticate(user=self.admin_user)  # type: ignore

#         url = reverse("list_create_cinema_view")
#         response = self.client.get(url)

#         cinemas = response.json()
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(len(cinemas) > 0)

#     def test_create_cinema_post_fail(self):
#         self.client.force_authenticate(user=self.normal_user)  # type: ignore

#         url = reverse("list_create_cinema_view")
#         data = {"name": "test movie", "city": "Accra", "country": "Ghana", "total_screen": 2}
#         response = self.client.post(url, data=data)

#         self.assertEqual(response.status_code, 403)

#     def test_create_cinema_post_success(self):
#         self.client.force_authenticate(user=self.admin_user)  # type: ignore

#         url = reverse("list_create_cinema_view")

#         data = {"name": "test movie", "city": "Accra", "country": "Ghana", "total_screen": 2}
#         response = self.client.post(url, data=data)

#         is_ava = Cinema.objects.filter(name="test movie").exists()

#         self.assertEqual(response.status_code, 201)
#         self.assertTrue(is_ava)

#     def test_retrieve_cinema_successful(self):
#         self.client.force_authenticate(user=self.admin_user)  # type: ignore

#         url = reverse("get_update_delete_cinema_view", args=[self.test_cinema.pk])
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, 200)

#     def test_update_cinema_successful(self):
#         self.client.force_authenticate(user=self.admin_user)  # type: ignore
#         data = {"name": "Man of steel"}
#         url = reverse("get_update_delete_cinema_view", args=[self.test_cinema.pk])
#         response = self.client.patch(url, data=data)

#         is_ava = Cinema.objects.filter(name="Man of steel").exists()

#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(is_ava)

#     def test_delete_cinema_successful(self):
#         self.client.force_authenticate(user=self.admin_user)  # type: ignore

#         url = reverse("get_update_delete_cinema_view", args=[self.test_cinema.pk])
#         response = self.client.delete(url)

#         is_ava = Cinema.objects.filter(name="local cinema").exists()

#         self.assertEqual(response.status_code, 204)
#         self.assertFalse(is_ava)


class ScreenTestCase(APITestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.admin_user = User.objects.create_user(
            username="testadmin", password="testpass123", role="admin"
        )
        self.normal_user = User.objects.create_user(username="test1admin", password="testpass123")
        self.cinema_obj = Cinema.objects.create(
            name="local cinema", city="Accra", country="Ghana", total_screen=2
        )

        self.screen_obj = Screen.objects.create(
            cinema_id=self.cinema_obj, total_seats=2, screen_number=f"cinema:{self.cinema_obj.pk}#1"
        )

    def test_cinema_signal_success(self):
        # create screen
        Screen.objects.create(
            cinema_id=self.cinema_obj, screen_number=f"cinema:{self.cinema_obj.pk}#2", total_seats=2
        )

        is_ava = Screen.objects.filter(screen_number=f"cinema:{self.cinema_obj.pk}#2").exists()
        self.assertTrue(is_ava)

    def test_list_screen_successful(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore

        url = reverse("list_create_screen_view", args=[self.cinema_obj.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_list_screen_fail(self):
        self.client.force_authenticate(user=self.normal_user)  # type: ignore

        url = reverse("list_create_screen_view", args=[self.cinema_obj.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_create_screen_success(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore

        data = {
            "cinema_id": self.cinema_obj.pk,
            "total_seats": 2,
            "screen_number": f"cinema:{self.cinema_obj.pk}#2",
        }
        url = reverse("list_create_screen_view", args=[self.cinema_obj.pk])
        response = self.client.post(url, data=data)
        is_ava = Screen.objects.filter(screen_number=f"cinema:{self.cinema_obj.pk}#2").exists()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(is_ava)

    def test_create_screen_fail_403(self):
        self.client.force_authenticate(user=self.normal_user)  # type: ignore

        data = {
            "cinema_id": self.cinema_obj.pk,
            "total_seats": 2,
            "screen_number": f"cinema:{self.cinema_obj.pk}#2",
        }
        url = reverse("list_create_screen_view", args=[self.cinema_obj.pk])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 403)

    def test_create_screen_fail_404(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore

        data = {
            "cinema_id": self.cinema_obj.pk,
            "total_seats": 2,
            "screen_number": f"cinema:{self.cinema_obj.pk}#2",
        }
        url = reverse("list_create_screen_view", args=[40])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 404)


    def test_update_screen_successful(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore

        data = {
            "total_seats": 12,
        }
        url = reverse("get_update_delete_screen_view", args=[self.cinema_obj.pk, self.screen_obj.pk])
        response = self.client.patch(url, data=data)

        try:
            screen = Screen.objects.get(screen_number=f"cinema:{self.cinema_obj.pk}#1")
        except Screen.DoesNotExist:
            self.fail()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(screen.total_seats == 12)

    def test_retrieve_screen_successful(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore

        url = reverse("get_update_delete_screen_view", args=[self.cinema_obj.pk, self.screen_obj.pk])
        response = self.client.get(url)

        data = response.json()["data"]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['total_seats'] == 2)

    def test_delete_screen_successful(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore

        url = reverse("get_update_delete_screen_view", args=[self.cinema_obj.pk, self.screen_obj.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)