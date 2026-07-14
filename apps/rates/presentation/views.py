from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.rates.domain.services import ExchangeRateService

class CurrentRatesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response(ExchangeRateService().get_current_rates())

class RateHistoryView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, currency_code):
        days = int(request.query_params.get('days', 7))
        return Response(ExchangeRateService().get_history(currency_code, days))