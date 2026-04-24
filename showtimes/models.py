import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from cinemas.models import Screen
from movies.models import Movie


# Create your models here.
class Showtime(models.Model):
    STATUS = (
        ('pending', "PENDING"),
        ('upcoming', "UPCOMING"),
        ('complete', 'COMPLETE')
    )
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen_id = models.ForeignKey(Screen, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=False)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    status = models.CharField(max_length=8, choices=STATUS, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.movie_id.title} at {self.start_time}"

    @property
    def end_time(self):
        return self.start_time + datetime.timedelta(minutes=self.movie_id.duration)

    def clean(self):
        # Prevent overlapping showtimes on the same screen
        if self.start_time and self.movie_id and self.screen_id:
            end_time = self.end_time
            overlapping_showtimes = Showtime.objects.filter(
                screen_id=self.screen_id,
                start_time__lt=end_time
            ).exclude(pk=self.pk)

            for showtime in overlapping_showtimes:
                if showtime.end_time > self.start_time:
                    raise ValidationError(
                        f"This showtime overlaps with {showtime.movie_id.title} "
                        f"({showtime.start_time.strftime('%H:%M')} - {showtime.end_time.strftime('%H:%M')})"
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = [
            "movie_id", "screen_id", "start_time"
        ]