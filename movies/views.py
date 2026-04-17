# Create your views here.
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .models import Movie
from .serializers import MovieSerializer


class MovieListCreateView(ListCreateAPIView):
    parser_classes = (FormParser, MultiPartParser,)
    permission_classes = (IsAuthenticated, )
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
