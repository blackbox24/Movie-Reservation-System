from rest_framework import serializers

from .models import Cinema


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
