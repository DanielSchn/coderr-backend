from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status


class RegistrationTest(APITestCase):

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
        
        user_exists = User.objects.filter(email="danjooo@danjooo.de").exists()
        self.assertTrue(user_exists)
        self.assertEqual(response.status_code, status.HTTP_200_OK)