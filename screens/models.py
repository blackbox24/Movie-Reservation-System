from django.db import models
from cinemas.models import Cinema

# Create your models here.
class Screen(models.Model):
    cinema_id = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    screen_number = models.CharField(max_length=20,null=False, blank=False)
    total_seats = models.IntegerField()

    def __str__(self):
        return f"Screen: #{self.screen_number}, cinema: #{self.cinema_id}"

    class Meta:
        indexes = [
            models.Index(
                fields=("cinema_id",),
            ),
        ]

        unique_together = [
            "cinema_id","screen_number"
        ]
