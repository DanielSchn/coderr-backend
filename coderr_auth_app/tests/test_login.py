from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status


class LoginTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )


    def test_login(self):
        url = reverse('login')
        data = {
            'username':'testuser',
            'password':'testpassword',
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_login_wrong_password(self):
        url = reverse('login')
        data = {
            'username':'testuser',
            'password':'testpaword',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['detail'], ['Falsche Anmeldedaten'])


    def test_login_wrong_username(self):
        url = reverse('login')
        data = {
            'username':'testr',
            'password':'testpassword',
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['detail'], ['Falsche Anmeldedaten'])