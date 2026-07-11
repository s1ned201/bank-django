from rest_framework import serializers
from apps.accounts.domain.dto import RegistrationDTO
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from apps.accounts.models import User
from apps.core.domain.exceptions import ValidationError
from apps.accounts.domain.services import TwoFAService
from apps.accounts.infrastructure.repositories import UserRepository
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    def to_dto(self) -> RegistrationDTO:
        validated_data = self.validated_data
        return RegistrationDTO(**validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Token Serializer
    Если у пользователя подтвержден Telegram не возвращает токены,
    а возвращает статус '2fa_required' и временный токен
    """

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password']
        }
        user = authenticate(**authenticate_kwargs)
        if user is None:
            raise ValidationError('Неверные учетные данные.')

        if user.telegram_id and user.is_telegram_verified:
            service = TwoFAService(UserRepository())
            service.send_code(user)
            refresh = RefreshToken.for_user(user)
            refresh['2fa_required'] = True
            refresh.set_exp(lifetime=timedelta(minutes=2))

            return {
                'status': '2fa_required',
                'temp_token': str(refresh.access_token),
            }
        else:
            data = super().validate(attrs)
            return data

class Verify2FASerializer(serializers.Serializer):
    temp_token = serializers.CharField()
    code = serializers.CharField(min_length=6, max_length=6)