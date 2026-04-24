from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer

class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

class BookingCancelView(generics.UpdateAPIView):
    """
    Allow users to cancel their own upcoming bookings.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user, status='confirmed')

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        
        # Only allow cancellation of upcoming showtimes
        if booking.showtime.start_time < timezone.now():
            return Response(
                {"detail": "Cannot cancel a booking for a past or ongoing showtime."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        booking.status = 'cancelled'
        booking.save()
        return Response({"detail": "Booking successfully cancelled."}, status=status.HTTP_200_OK)
