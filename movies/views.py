# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from utils.helpers import AdminOrReadOnly

from .models import Movie
from .serializers import MovieSerializer


class MovieListCreateView(ListCreateAPIView):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    permission_classes = (
        IsAuthenticated,
        AdminOrReadOnly,
    )
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

class MovieGetUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    permission_classes = (
        IsAuthenticated,
        AdminOrReadOnly,
    )
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    lookup_field = "id"
