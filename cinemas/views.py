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
        try:
            _ = Screen.objects.get(id=id)
        except Screen.DoesNotExist:
            return Response({"detail": "Cinema does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if self.check_permissions(request):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        screens = Screen.objects.filter(cinema_id=id)
        data = self.serializer_class(screens, many=True).data
        return Response({"data": data}, status=status.HTTP_200_OK)

    def post(self, request, id, *args, **kwargs):
        try:
            query = Screen.objects.get(id=id)
        except Screen.DoesNotExist:
            return Response({"detail": "Cinema does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if self.check_object_permissions(request, obj=query):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # check it the number of
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
        try:
            screen = Screen.objects.get(id=id)
        except Screen.DoesNotExist:
            return Response({"detail": "Screen does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            _ = Cinema.objects.get(id=cinema_id)
        except Screen.DoesNotExist:
            return Response({"detail": "Cinema does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if self.check_permissions(request):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        data = self.serializer_class(screen).data
        return Response({"data": data}, status=status.HTTP_200_OK)

    def patch(self, request, cinema_id,id, *args, **kwargs):
        try:
            screen = Screen.objects.get(id=id)
        except Screen.DoesNotExist:
            return Response({"detail": "Screen does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            _ = Cinema.objects.get(id=cinema_id)
        except Screen.DoesNotExist:
            return Response({"detail": "Cinema does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if self.check_object_permissions(request, obj=screen):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ScreenUpdateSerializer(data=request.data)
        if serializer.is_valid():
            # check it the number of
            total_seats = serializer.validated_data['total_seats'] # type: ignore
            screen.total_seats = total_seats
            screen.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, cinema_id, id, *args, **kwargs):
        try:
            screen = Screen.objects.get(id=id)
        except Screen.DoesNotExist:
            return Response({"detail": "Screen does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            _ = Cinema.objects.get(id=cinema_id)
        except Screen.DoesNotExist:
            return Response({"detail": "Cinema does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if self.check_object_permissions(request, obj=screen):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        screen.delete()
        return Response({"detail": "Successful"}, status=status.HTTP_204_NO_CONTENT)
