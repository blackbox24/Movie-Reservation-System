from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.helpers import AdminOrReadOnly

from .models import Cinema, Screen
from .serializers import CinemaSerializer, ScreenSerializer, ScreenUpdateSerializer


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


class ScreenListCreateView(APIView):
    permission_classes = (
        IsAuthenticated,
        AdminOrReadOnly,
    )
    serializer_class = ScreenSerializer

    def get(self, request, id, *args, **kwargs):
        cinema = get_object_or_404(Cinema, id=id)
        screens = Screen.objects.filter(cinema_id=cinema)
        data = self.serializer_class(screens, many=True).data
        return Response({"data": data}, status=status.HTTP_200_OK)

    def post(self, request, id, *args, **kwargs):
        get_object_or_404(Cinema, id=id)

        # Ensure cinema_id in request data matches the URL parameter if provided
        data = request.data.copy()
        data["cinema_id"] = id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScreenRetrieveUpdateDeleteView(APIView):
    permission_classes = (
        IsAuthenticated,
        AdminOrReadOnly,
    )
    serializer_class = ScreenSerializer

    def get(self, request, cinema_id, id, *args, **kwargs):
        get_object_or_404(Cinema, id=cinema_id)
        screen = get_object_or_404(Screen, id=id, cinema_id=cinema_id)
        data = self.serializer_class(screen).data
        return Response({"data": data}, status=status.HTTP_200_OK)

    def patch(self, request, cinema_id, id, *args, **kwargs):
        get_object_or_404(Cinema, id=cinema_id)
        screen = get_object_or_404(Screen, id=id, cinema_id=cinema_id)

        serializer = ScreenUpdateSerializer(data=request.data)
        if serializer.is_valid():
            total_seats = serializer.validated_data["total_seats"]
            screen.total_seats = total_seats
            screen.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cinema_id, id, *args, **kwargs):
        get_object_or_404(Cinema, id=cinema_id)
        screen = get_object_or_404(Screen, id=id, cinema_id=cinema_id)
        screen.delete()
        return Response({"detail": "Successful"}, status=status.HTTP_204_NO_CONTENT)
