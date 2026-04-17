from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField()
    duration = models.TimeField(null=False)
    rating = models.IntegerField(default=0)
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
            models.Index(fields=("title",),),
        ]
        ordering = ["-created_at"]
