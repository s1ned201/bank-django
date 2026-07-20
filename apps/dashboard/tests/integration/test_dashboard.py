import pytest

@pytest.mark.django_db
class TestDashboardAPI:
    def test_get_dashboard(self, auth_client, accounts):
        response = auth_client.get('/api/v1/dashboard/')
        assert response.status_code == 200
        data = response.json()
        assert 'accounts' in data
        assert len(data['accounts']) == 2

    def test_get_transactions(self, auth_client, accounts):
        acc1, _ = accounts
        response = auth_client.get(f'/api/v1/dashboard/transactions/?account_id={acc1.id}&limit=10')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['type'] == 'transfer'