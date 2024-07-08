from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class OrganizationTests(APITestCase):

    def setUp(self):
        self.register_url = f'/api/auth/register'
        self.login_url = f'/api/auth/login'
        self.user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.token = response.data['data']['accessToken']
        self.userId = response.data['data']['user']['userId']

    def test_get_user_details(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        user_url = f"/api/users/{self.userId}"
        
        response = self.client.get(user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['userId'], self.userId)

    def test_get_user_organizations(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        orgs_url = f'/api/organisations'

        response = self.client.get(orgs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(len(response.data['data']['organisations']), 1)
        self.assertEqual(response.data['data']['organisations'][0]['name'], "John's Organisation")

    def test_create_organization(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        create_org_url = reverse('user_orgs')
        
        org_data = {
            "name": "John's Second Organisation",
            "description": "Another organization"
        }
        response = self.client.post(create_org_url, org_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['name'], "John's Second Organisation")

    def test_add_user_to_organization(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        new_user = {
            "firstName": "Chris",
            "lastName": "Adebiyi",
            "email": "hi.chrisdev@example.com",
            "password": "password123",
            "phone": "8161201965"
        }
        register = self.client.post(self.register_url, new_user, format='json')
        
        org_id = 1
        add_user_url = reverse('add_user', args=[org_id])
        user_data = {
            "userId": register.data['data']['user']['userId']
        }
        
        response = self.client.post(add_user_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'User added to organization successfully')