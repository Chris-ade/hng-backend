import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    url = '/api/auth/register'
    data = {
        "userId": "uniqueUserId",
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['status'] == 'success'
    assert response.data['data']['user']['firstName'] == "John"
    assert response.data['data']['user']['lastName'] == "Doe"

@pytest.mark.django_db
def test_user_login():
    client = APIClient()
    register_url = '/api/auth/register'
    login_url = '/api/auth/login'
    data = {
        "userId": "uniqueUserId",
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    }
    client.post(register_url, data, format='json')
    response = client.post(login_url, {"email": "john.doe@example.com", "password": "password123"}, format='json')
    assert response.status_code == 200
    assert response.data['status'] == 'success'