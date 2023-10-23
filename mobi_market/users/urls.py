from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .endpoints import UserCreateAPIView, UserProfileAPIView, SetPhoneNumberAPIView, PhoneNumberActivateAPIView


urlpatterns = [
    path("api/register/", UserCreateAPIView.as_view(), name="register"),
    path("api/user/profile/", UserProfileAPIView.as_view(), name="user_profile"),
    path("api/user/set_phone_number/", SetPhoneNumberAPIView.as_view(), name="set_user_phone_number"),
    path("api/user/activate_phone_number/", PhoneNumberActivateAPIView.as_view(), name="activate_user_phone_number"),
    path('api/token/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
