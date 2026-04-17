from django.urls import path

from . import views

urlpatterns = [
    path("", views.MovieListCreateView.as_view(), name="list_create_movie_view"),
    path(
        "<int:id>/", views.MovieGetUpdateDeleteView.as_view(), name="get_update_delete_movie_view"
    ),
]
