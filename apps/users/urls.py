from django.urls import path
from rest_framework import routers

from apps.users.views import (
    SignupAPI,
    ActivationAPI,
    LoginAPI,
    LogoutAPI,
    UserAPI,
    ForgotPasswordAPI,
    IinAPI,
)


router = routers.DefaultRouter()


urlpatterns = [
    path("user/", UserAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("logout/", LogoutAPI.as_view()),
    path("signup/", SignupAPI.as_view()),
    path("activate/", ActivationAPI.as_view()),
    path("reset-password/", ForgotPasswordAPI.as_view()),
    path("iin/", IinAPI.as_view()),
]
