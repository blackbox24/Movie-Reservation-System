from rest_framework import serializers
from .models import Showtime

class ShowtimeSerializer(serializers.ModelSerializer):
    movie_title = serializers.ReadOnlyField(source='movie_id.title')
    screen_number = serializers.ReadOnlyField(source='screen_id.screen_number')
    cinema_name = serializers.ReadOnlyField(source='screen_id.cinema_id.name')

    class Meta:
        model = Showtime
        fields = [
            'id', 'movie_id', 'movie_title', 'screen_id', 'screen_number', 
            'cinema_name', 'start_time', 'base_price', 'status', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
