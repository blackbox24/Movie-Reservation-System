from rest_framework import serializers

from cinemas.models import Cinema
from .models import Screen


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = [
            "id","cinema_id","screen_number","total_seat"
        ]
        read_only_fields = [
            "id"
        ]

    def validate(self, attrs):
        data =  super().validate(attrs)
        cinema_id = attrs.get("cinema_id","")
        try:
            Cinema.objects.get(id=cinema_id)
        except Cinema.DoesNotExist as e:
            return serializers.ValidationError(detail=f"Cinema does not exist: {e}")

        return data
