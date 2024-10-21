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