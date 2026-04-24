import datetime

from rest_framework import serializers

from .models import Showtime


class ShowtimeSerializer(serializers.ModelSerializer):
    movie_title = serializers.ReadOnlyField(source="movie_id.title")
    screen_number = serializers.ReadOnlyField(source="screen_id.screen_number")
    cinema_name = serializers.ReadOnlyField(source="screen_id.cinema_id.name")

    class Meta:
        model = Showtime
        fields = [
            "id",
            "movie_id",
            "movie_title",
            "screen_id",
            "screen_number",
            "cinema_name",
            "start_time",
            "base_price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        # We need to handle both creation and partial updates
        movie = data.get("movie_id") or (self.instance.movie_id if self.instance else None)
        screen = data.get("screen_id") or (self.instance.screen_id if self.instance else None)
        start_time = data.get("start_time") or (self.instance.start_time if self.instance else None)

        if movie and screen and start_time:
            end_time = start_time + datetime.timedelta(minutes=movie.duration)

            overlapping_showtimes = Showtime.objects.filter(
                screen_id=screen, start_time__lt=end_time
            )

            if self.instance:
                overlapping_showtimes = overlapping_showtimes.exclude(pk=self.instance.pk)

            for showtime in overlapping_showtimes:
                if showtime.end_time > start_time:
                    raise serializers.ValidationError(
                        f"This showtime overlaps with {showtime.movie_id.title} "
                        f"({showtime.start_time.strftime('%H:%M')} - {showtime.end_time.strftime('%H:%M')})"
                    )
        return data
