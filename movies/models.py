from django.db import models

from users.models import User


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField()
    duration = models.TimeField(null=False)
    poster = models.ImageField(upload_to="posters")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self, *args, **kwargs):
        return f"Movie: {self.title}"

    def get_poster_url(self):
        if self.poster.url == "" or self.poster is None:
            return "https://images.unsplash.com/photo-1661495896705-dce1b43030b0?ixid=M3w4MjcwNjd8MHwxfHNlYXJjaHwxODF8fGFuaW1lJTIwd2FsbHBhcGVyfGVufDB8fHx8MTc3NjQzNzc3Mnww&ixlib=rb-4.1.0&fit=max&q=80"
        return self.poster.url

    class Meta:
        indexes = [
            models.Index(
                fields=("title",),
            ),
        ]
        ordering = ["-created_at"]


class Rating(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()

    def __str__(self):
        return f"{self.user_id.username}'s Rate: {self.rate}"

    class Meta:
        unique_together = ["movie_id", "user_id"]
