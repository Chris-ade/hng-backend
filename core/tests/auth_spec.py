from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class AuthTests(APITestCase):

    def test_register_user_successfully(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['user']['firstName'], "John")
        self.assertEqual(response.data['data']['user']['lastName'], "Doe")

    def test_register_user_missing_fields(self):
        url = reverse('register')
        data = {
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertTrue(any(error['field'] == 'firstName' for error in response.data['errors']))

    def test_register_user_duplicate_email(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.client.post(url, data, format='json')
        data['userId'] = 2
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertTrue(any(error['field'] == 'email' for error in response.data['errors']))

    def test_login_user_successfully(self):
        register_url = reverse('register')
        login_url = reverse('login')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.client.post(register_url, data, format='json')
        response = self.client.post(login_url, {"email": "john.doe@example.com", "password": "password123"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('accessToken', response.data['data'])

    def test_login_user_invalid_credentials(self):
        register_url = reverse('register')
        login_url = reverse('login')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.client.post(register_url, data, format='json')
        response = self.client.post(login_url, {"email": "john.doe@example.com", "password": "wrongpassword"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Authentication failed')