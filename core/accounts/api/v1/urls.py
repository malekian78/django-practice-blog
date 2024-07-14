from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


app_name = "api-v1"


router = routers.DefaultRouter()
router.register("profile", views.ProfileViewSet, basename="profile")

urlpatterns = [
    # دوباره فرستادن ایمیل به کاربر
    path("verify/resend/", views.VerificationEmail.as_view(), name="email_resend"),
    # احراز هویت
    path("verify-email/", views.VerificationEmail.as_view(), name="email_verify"),
    path(
        "verify/confirm/<str:token>/",
        views.UserVerificationViewSet.as_view(),
        name="user_verify",
    ),
    
    # jwt
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path(
        "change-password/",
        views.ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    # Token
    path("token/login/", ObtainAuthToken.as_view(), name="token_login"),
    path("token/logout/", views.CustomDiscardAuthToken.as_view(), name="token_logout"),

]

urlpatterns += router.urls