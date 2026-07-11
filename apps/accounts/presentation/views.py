from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from apps.accounts.presentation.serializers import RegistrationSerializer, Verify2FASerializer
from apps.accounts.domain.services import RegistrationService, TwoFAService
from apps.accounts.infrastructure.repositories import UserRepository
from apps.core.domain.exceptions import ValidationError

from .serializers import CustomTokenObtainPairSerializer

class RegistrationView(APIView):

    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = serializer.to_dto()
        service = RegistrationService(UserRepository())
        user = service.execute(dto)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class Verify2FAView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = Verify2FASerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        temp_token = serializer.validated_data['temp_token']
        code = serializer.validated_data['code']

        try:
            access_token = AccessToken(temp_token)
            if not access_token.get('2fa_required'):
                raise ValidationError('Токен не предназначен для 2FA.')
            user_id = access_token['user_id']
        except Exception as e:
            raise ValidationError('Недействительный временный токен.')

        user_repo = UserRepository()
        user = user_repo.get_by_id(user_id)
        twofa_service = TwoFAService(user_repo)
        ip = request.META.get('REMOTE_ADDR')
        twofa_service.verify_code(user, code, ip)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })