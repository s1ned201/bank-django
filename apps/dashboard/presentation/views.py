from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.dashboard.domain.services import DashboardService

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

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