import pytest

@pytest.mark.django_db
class TestAssistantAPI:
    def test_greeting(self, auth_client):
        response = auth_client.post('/api/v1/assistant/', {'message': 'привет'}, format='json')
        assert response.status_code == 200
        data = response.json()
        assert 'Здравствуйте' in data['response']

    def test_rates_keyword(self, auth_client, currencies_and_rates):
        response = auth_client.post('/api/v1/assistant/', {'message': 'курсы'}, format='json')
        assert response.status_code == 200
        data = response.json()
        assert 'USD' in data['response']
        assert 'EUR' in data['response']

    def test_conversion(self, auth_client, currencies_and_rates):
        response = auth_client.post('/api/v1/assistant/', {'message': '100 usd в eur'}, format='json')
        assert response.status_code == 200
        data = response.json()
        assert 'EUR' in data['response']

    def test_conversion_byn(self, auth_client, currencies_and_rates):
        response = auth_client.post('/api/v1/assistant/', {'message': '100 usd в byn'}, format='json')
        assert response.status_code == 200
        data = response.json()
        assert 'BYN' in data['response']