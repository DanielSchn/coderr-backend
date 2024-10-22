from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from coderr_app.models import UserProfile

class ProfileDetailTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@test.de')

        self.user_profile = UserProfile.objects.create(
            user=self.user,
            email=self.user.email,
            location="Berlin",
            tel="123456789",
            description="Business description",
            working_hours="9-17",
            type="business",
            created_at="2023-01-01T12:00:00"
        )


    def test_get_profile_details(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], 'Berlin')