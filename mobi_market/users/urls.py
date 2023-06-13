from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .endpoints import UserCreateAPIView


urlpatterns = [
    path("api/register/", UserCreateAPIView.as_view(), name="register"),
    path('api/token/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
