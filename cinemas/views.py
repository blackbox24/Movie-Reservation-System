
# Create your views here.
# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from utils.helpers import AdminOrReadOnly

from .models import Cinema
from .serializers import CinemaSerializer


class CinemaListCreateView(ListCreateAPIView):
    permission_classes = (
        IsAuthenticated,
        AdminOrReadOnly,
    )
    serializer_class = CinemaSerializer
    queryset = Cinema.objects.all()


class CinemaGetUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        AdminOrReadOnly,
    )
    serializer_class = CinemaSerializer
    queryset = Cinema.objects.all()
    lookup_field = "id"
