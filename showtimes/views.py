from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from utils.helpers import AdminOrReadOnly

from .models import Showtime
from .serializers import ShowtimeSerializer


class ShowtimeListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, AdminOrReadOnly)
    serializer_class = ShowtimeSerializer
    queryset = Showtime.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        movie_id = self.request.query_params.get("movie_id")
        date = self.request.query_params.get("date")

        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        if date:
            queryset = queryset.filter(start_time__date=date)

        return queryset


class ShowtimeRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AdminOrReadOnly)
    serializer_class = ShowtimeSerializer
    queryset = Showtime.objects.all()
    lookup_field = "id"
