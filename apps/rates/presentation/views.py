from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.rates.domain.services import ExchangeRateService
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class CurrentRatesView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: OpenApiResponse(response=OpenApiTypes.OBJECT, description="Текущие курсы валют"),
        },
        description="Получение текущих курсов НБ РБ (BYN за 1 единицу валюты)",
    )

    def get(self, request):
        return Response(ExchangeRateService().get_current_rates())

class RateHistoryView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="days", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, default=7),
        ],
        responses={
            200: OpenApiResponse(response=OpenApiTypes.OBJECT, description="История курса валюты"),
            404: OpenApiResponse(description="Валюта не найдена"),
        },
        description="История курса конкретной валюты за последние N дней",
    )

    def get(self, request, currency_code):
        days = int(request.query_params.get('days', 7))
        return Response(ExchangeRateService().get_history(currency_code, days))