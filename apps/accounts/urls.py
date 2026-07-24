from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .presentation.views import (
    RegistrationView,
    CustomTokenObtainPairView,
    Verify2FAView,
    TelegramBindView,
    TelegramVerifyView,
    ProfileView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-2fa/', Verify2FAView.as_view(), name='verify_2fa'),
    path('telegram/bind/', TelegramBindView.as_view(), name='telegram_bind'),
    path('telegram/verify/', TelegramVerifyView.as_view(), name='telegram_verify'),
    path('profile/', ProfileView.as_view(), name='profile'),
]