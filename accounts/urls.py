from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup_view"),
    path("login/", TokenObtainPairView.as_view(), name="login_view"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh_token_view"),
]
