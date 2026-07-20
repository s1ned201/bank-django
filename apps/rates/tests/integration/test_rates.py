import pytest
from django.core.cache import cache

@pytest.mark.django_db
class TestRatesAPI:
    def test_current_rates(self, api_client, currencies_and_rates):
        cache.clear()
        response = api_client.get('/api/v1/rates/')
        assert response.status_code == 200
        data = response.json()
        assert 'USD' in data
        assert 'EUR' in data
        assert data['USD']['code'] == 'USD'
        assert 'rate' in data['USD']

    def test_rate_history(self, api_client, currencies_and_rates):
        response = api_client.get('/api/v1/rates/history/USD/?days=5')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 6