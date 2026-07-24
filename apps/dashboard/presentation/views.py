from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.dashboard.domain.services import DashboardService
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from apps.dashboard.models import Account, Transaction
from apps.rates.models import Currency
from apps.core.domain.exceptions import ValidationError

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

class CreateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name', 'Основной')
        currency_code = request.data.get('currency')
        if not currency_code:
            return Response({'error': 'Валюта обязательна'}, status=400)
        try:
            currency = Currency.objects.get(code=currency_code.upper())
        except Currency.DoesNotExist:
            return Response({'error': f'Валюта {currency_code} не найдена'}, status=404)
        account = Account.objects.create(user=request.user, currency=currency, name=name)
        return Response({
            'id': account.id,
            'name': account.name,
            'currency': account.currency.code,
            'balance': str(account.balance)
        }, status=201)

class CreateTransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from_account_id = request.data.get('from_account')
        to_account_id = request.data.get('to_account')
        amount = request.data.get('amount')
        description = request.data.get('description', '')

        if not from_account_id or not to_account_id or not amount:
            raise ValidationError("from_account, to_account и amount обязательны")

        try:
            amount = float(amount)
        except ValueError:
            raise ValidationError("Неверная сумма")

        if amount <= 0:
            raise ValidationError("Сумма должна быть положительной")

        try:
            from_account = Account.objects.get(pk=from_account_id, user=request.user)
        except Account.DoesNotExist:
            raise ValidationError("Счет отправителя не найден или не принадлежит вам")

        try:
            to_account = Account.objects.get(pk=to_account_id, user=request.user)
        except Account.DoesNotExist:
            raise ValidationError("Счет получателя не найден или не принадлежит вам")

        if from_account == to_account:
            raise ValidationError("Нельзя перевести на тот же счет")

        if from_account.balance < amount:
            raise ValidationError("Недостаточно средств")

        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()

        transaction = Transaction.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount,
            transaction_type='transfer',
            description=description
        )

        return Response({
            'id': transaction.id,
            'type': transaction.transaction_type,
            'amount': str(transaction.amount),
            'from_account': transaction.from_account_id,
            'to_account': transaction.to_account_id,
            'description': transaction.description,
            'date': transaction.created_at.isoformat(),
        }, status=201)