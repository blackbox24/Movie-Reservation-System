from rest_framework import serializers

from .models import Cinema, Screen


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ["id", "cinema_id", "screen_number", "total_seats"]
        read_only_fields = ["id"]
