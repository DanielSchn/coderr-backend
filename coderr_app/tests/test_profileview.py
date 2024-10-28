from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from coderr_app.models import UserProfile
from rest_framework.authtoken.models import Token

class ProfileDetailTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@test.de')
        self.user_2 = User.objects.create_user(username='testuser2', password='testpassword2', email='test2@test.de')
        self.admin_user = User.objects.create_superuser(username='admin', password='wasd')
        
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            email=self.user.email,
            location="Berlin User",
            tel="123456789",
            description="Business description",
            working_hours="9-17",
            type="business",
            created_at="2023-01-01T12:00:00"
        )
        self.user_profile_2 = UserProfile.objects.create(
            user=self.user_2,
            email=self.user_2.email,
            location="Berlin User 2",
            tel="123456789",
            description="Business description",
            working_hours="9-17",
            type="business",
            created_at="2023-01-01T12:00:00"
        )

        self.token_user = Token.objects.create(user=self.user)
        self.token_user_2 = Token.objects.create(user=self.user_2)
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.client = APIClient()


    def test_get_profile_details_as_not_owner(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_get_profile_details_as_unauthorized(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_profile_details_as_admin(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_profile_details_as_owner(self):
        url = reverse('profile-detail', kwargs={'pk': self.user_2.pk})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], 'Berlin User 2')


    def test_patch_profile_details_as_owner(self):
        url = reverse('profile-detail', kwargs={'pk': self.user_2.pk})

        data = {
            'location': "Berlin Patch"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], 'Berlin Patch')


    def test_patch_profile_details_as_admin(self):
        url = reverse('profile-detail', kwargs={'pk': self.user_2.pk})

        data = {
            'location': "Berlin Patch"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], 'Berlin Patch')


    def test_patch_profile_details_as_unauthorized(self):
        url = reverse('profile-detail', kwargs={'pk': self.user_2.pk})

        data = {
            'location': "Berlin Patch"
        }

        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
