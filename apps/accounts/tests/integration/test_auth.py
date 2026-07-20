import pytest
from apps.accounts.models import User, TwoFACode


@pytest.mark.django_db
class TestAuth:
    def test_registration_success(self, api_client):
        response = api_client.post('/api/v1/auth/register/',{
            'username': 'newuser',
            'password': 'strongp@ss',
            'email': 'new@example.com',
            'first_name': 'Test',
        })
        assert response.status_code == 201
        assert User.objects.filter(username='newuser').exists()

    def test_registration_duplicate(self, api_client, user):
        response = api_client.post('/api/v1/auth/register/',{
            'username': 'testuser',
            'email': 'dup@example.com',
            'password': 'strongp@ss',
        })
        assert response.status_code == 409

    def test_token_2fa_required(self, api_client, user):
        response = api_client.post('/api/v1/auth/token/',{
            'username': 'testuser',
            'password': 'strongp@ss',
        })
        assert response.status_code == 200
        assert response.json()['status'] == '2fa_required'
        assert 'temp_token' in response.json()

    def test_verify_2fa_and_get_tokens(self, api_client, user):
        token_response = api_client.post('/api/v1/auth/token/',{
            'username': 'testuser',
            'password': 'strongp@ss',
        })
        temp_token = token_response.json()['temp_token']
        code = TwoFACode.objects.filter(user=user, is_used=False).latest('created_at').code
        response = api_client.post('/api/v1/auth/verify-2fa/',{
            'temp_token': temp_token,
            'code': code,
        })
        assert response.status_code == 200
        data = response.json()
        assert 'access' in data
        assert 'refresh' in data

    def test_token_no_2fa(self, api_client, user):
        user.telegram_id = None
        user.save()
        response = api_client.post('/api/v1/auth/token/',{
            'username': 'testuser',
            'password': 'strongp@ss',
        })
        assert response.status_code == 200
        assert response.json()
        assert 'access' in response.json()