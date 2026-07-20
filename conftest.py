import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User
from datetime import date, timedelta
from apps.rates.models import Currency, ExchangeRate
from apps.dashboard.models import Account, Transaction

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', email='strong@ss', password='strongp@ss')
    user.telegram_id = 123456789
    user.is_telegram_verified = True
    user.save()
    return user

@pytest.fixture
def auth_client(api_client, user):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

@pytest.fixture
def currencies_and_rates(db):
    usd = Currency.objects.create(code='USD', name='US Dollar', symbol='$')
    eur = Currency.objects.create(code='EUR', name='Euro', symbol='€')
    today = date.today()
    for i in range(7):
        d = today - timedelta(days=i)
        ExchangeRate.objects.create(currency=usd, rate=2.5 + i*0.01, date=d)
        ExchangeRate.objects.create(currency=eur, rate=3.0 + i*0.01, date=d)
    return usd, eur

@pytest.fixture
def accounts(user, currencies_and_rates):
    usd, eur = currencies_and_rates
    acc1 = Account.objects.create(user=user, currency=usd, balance=1000.00, name='USD Account')
    acc2 = Account.objects.create(user=user, currency=eur, balance=500.00, name='EUR Account')
    Transaction.objects.create(from_account=acc1, to_account=acc2, amount=100, transaction_type='transfer', description='Test transfer')
    return acc1, acc2