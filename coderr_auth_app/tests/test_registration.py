from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from coderr_auth_app.api.serializers import RegistrationSerializer


class RegistrationTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.de', password='testpassword')


    def test_registration(self):
        url = reverse('registration')
        data = {
            'username':'danjooo',
            'password':'asdasd',
            'repeated_password':'asdasd',
            'email':'danjooo@danjooo.de',
            'type':'customer'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_registration_username_exists(self):
        url = reverse('registration')
        data = {
            'username': 'testuser',
            'password': 'asdasd',
            'repeated_password': 'asdasd',
            'email': 'danjooo@danjooo.de',
            'type': 'customer'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['username'], ['Dieser Benutzername ist bereits vergeben.'])


    def test_registration_email_exists(self):
        url = reverse('registration')
        data = {
            'username': 'test',
            'password': 'asdasd',
            'repeated_password': 'asdasd',
            'email': 'test@test.de',
            'type': 'customer'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'], ['Diese E-Mail-Adresse wird bereits verwendet.'])

    
    def test_registration_password_unequal(self):
        url = reverse('registration')
        data = {
            'username': 'test1',
            'password': 'asdasd',
            'repeated_password': 'asdas',
            'email': 'test1@test.de',
            'type': 'customer'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['password'], ['Die Passwörter sind nicht identisch.'])