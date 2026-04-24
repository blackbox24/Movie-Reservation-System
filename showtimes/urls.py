from django.urls import path

from . import views

urlpatterns = [
    path("", views.ShowtimeListCreateView.as_view(), name="showtime-list-create"),
    path("<int:id>/", views.ShowtimeRetrieveUpdateDeleteView.as_view(), name="showtime-detail"),
]
