from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.dashboard.domain.services import DashboardService
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="account_id", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, description="ID счета"),
            OpenApiParameter(name="limit", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, default=20),
        ],
        responses={
            200: OpenApiResponse(response=OpenApiTypes.OBJECT, description="История транзакций"),
            400: OpenApiResponse(description="Не указан account_id"),
        },
        description="Получение последних транзакций по счёту",
    )

    @extend_schema(
        responses={
            200: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Список счетов пользователя"),
        },
        description="Получение информации о счетах текущего пользователя",
    )

    def get(self, request):
        service = DashboardService()
        return Response(service.get_dashboard_data(request.user))

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account_id = request.query_params.get('account_id')
        if not account_id:
            return Response(
                {'error': 'Параметр "account_id" обязателен'},
                status=400
            )
        limit = int(request.query_params.get('limit', 20))
        service = DashboardService()
        return Response(service.get_transactions(request.user, account_id, limit))