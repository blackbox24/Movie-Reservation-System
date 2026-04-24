from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from .models import Booking, Ticket
from showtimes.models import Showtime

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['seat_row', 'seat_number']

class BookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    movie_title = serializers.ReadOnlyField(source='showtime.movie_id.title')
    start_time = serializers.ReadOnlyField(source='showtime.start_time')

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'showtime', 'movie_title', 'start_time', 
            'total_amount', 'status', 'qr_code', 'tickets', 'created_at'
        ]
        read_only_fields = ['id', 'total_amount', 'status', 'qr_code', 'created_at']

    def validate(self, data):
        showtime = data['showtime']
        tickets_data = data['tickets']

        # 1. Validate showtime is in the future
        if showtime.start_time < timezone.now():
            raise serializers.ValidationError("Cannot book tickets for past showtimes.")

        # 2. Validate seat availability (capacity)
        if len(tickets_data) > showtime.remaining_seats:
            raise serializers.ValidationError(
                f"Not enough seats available. Remaining: {showtime.remaining_seats}"
            )

        # 3. Validate specific seat availability
        for ticket in tickets_data:
            if Ticket.objects.filter(
                booking__showtime=showtime,
                booking__status='confirmed',
                seat_row=ticket['seat_row'],
                seat_number=ticket['seat_number']
            ).exists():
                raise serializers.ValidationError(
                    f"Seat {ticket['seat_row']}{ticket['seat_number']} is already booked."
                )

        return data

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        showtime = validated_data['showtime']
        
        # Calculate total amount
        total_amount = showtime.base_price * len(tickets_data)
        validated_data['total_amount'] = total_amount
        
        booking = Booking.objects.create(**validated_data)
        
        for ticket_data in tickets_data:
            Ticket.objects.create(booking=booking, **ticket_data)
            
        return booking
