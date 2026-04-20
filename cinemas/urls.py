from django.urls import path

from . import views

urlpatterns = [
    path("", views.CinemaListCreateView.as_view(), name="list_create_cinema_view"),
    path(
        "<int:id>/", views.CinemaGetUpdateDeleteView.as_view(), name="get_update_delete_cinema_view"
    ),
    path("<int:id>/screens/", views.ScreenListCreateView.as_view(), name="list_create_screen_view"),
    path(
        "<int:cinema_id>/screens/<int:id>/",
        views.ScreenRetrieveUpdateDeleteView.as_view(),
        name="get_update_delete_screen_view",
    ),
]
