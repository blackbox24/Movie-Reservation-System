import datetime
from decimal import Decimal

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from cinemas.models import Cinema, Screen
from movies.models import Movie
from showtimes.models import Showtime
from users.models import User


class ShowtimeTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin", password="password123", role="admin"
        )
        self.normal_user = User.objects.create_user(
            username="user", password="password123", role="user"
        )
        self.movie = Movie.objects.create(
            title="Inception", description="Dream within a dream", duration=148
        )
        self.cinema = Cinema.objects.create(
            name="Cinema 1", city="New York", country="USA", total_screen=5
        )
        self.screen = Screen.objects.create(
            cinema_id=self.cinema, screen_number="1", total_seats=100
        )

        self.start_time = timezone.now() + datetime.timedelta(days=1)
        self.showtime = Showtime.objects.create(
            movie_id=self.movie,
            screen_id=self.screen,
            start_time=self.start_time,
            base_price=Decimal("10.00"),
        )

    def test_list_showtimes(self):
        url = reverse("showtime-list-create")
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Account for pagination
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 1)

    def test_create_showtime_admin_only(self):
        url = reverse("showtime-list-create")
        data = {
            "movie_id": self.movie.id,
            "screen_id": self.screen.id,
            "start_time": (self.start_time + datetime.timedelta(hours=5)).isoformat(),
            "base_price": "15.00",
        }

        # Test Normal User Fail
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

        # Test Admin Success
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_overlap_prevention(self):
        url = reverse("showtime-list-create")
        self.client.force_authenticate(user=self.admin_user)

        overlap_start = self.start_time + datetime.timedelta(hours=1)
        data = {
            "movie_id": self.movie.id,
            "screen_id": self.screen.id,
            "start_time": overlap_start.isoformat(),
            "base_price": "12.00",
        }

        response = self.client.post(url, data)
        # Now returns 400 because validation is in serializer
        self.assertEqual(response.status_code, 400)
        self.assertIn("overlaps", str(response.data))

    def test_filter_showtimes_by_date(self):
        url = reverse("showtime-list-create")
        self.client.force_authenticate(user=self.normal_user)

        today = timezone.now().date()
        response = self.client.get(url, {"date": today})
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 0)

        tomorrow = self.start_time.date()
        response = self.client.get(url, {"date": tomorrow})
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 1)
