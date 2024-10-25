from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from coderr_app.models import UserProfile, Offers, OfferDetails
from rest_framework.authtoken.models import Token


class OffersTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@test.de')

        self.offer = Offers.objects.create(
            user=self.user,
            title='Testoffer',
            description='Testdescription',
        )
        self.detail1 = OfferDetails.objects.create(
            offer=self.offer,
            title='Detail 1',
            revisions=2,
            delivery_time_in_days=5,
            price=100.00,
            features=["Feature 1", "Festure 2"],
            offer_type='basic'
        )
        self.detail2 = OfferDetails.objects.create(
            offer=self.offer,
            title='Standard Design',
            revisions=5,
            delivery_time_in_days=7,
            price=200.00,
            features=["Logo Design", "Visitenkarte", "Briefpapier"],
            offer_type='standard'
        )
        self.detail3 = OfferDetails.objects.create(
            offer=self.offer,
            title='Premium Design',
            revisions=10,
            delivery_time_in_days=10,
            price=500.00,
            features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
            offer_type='premium'
        )

        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

        
    def test_offer_creation_as_business_user(self):
        url = reverse('offers-list')
        data = {
            "title": "Online Marketing Paket",
            "description": "Maximieren Sie Ihre Reichweite online.",
            "details": [
                {
                    "title": "Basic Online Marketing",
                    "revisions": 1,
                    "delivery_time_in_days": 5,
                    "price": 100.00,
                    "features": ["1 Werbekampagne", "Woche"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Online Marketing",
                    "revisions": 3,
                    "delivery_time_in_days": 15,
                    "price": 250.00,
                    "features": ["3 Werbekampagnen", "2 Wochen"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Online Marketing",
                    "revisions": 5,
                    "delivery_time_in_days": 30,
                    "price": 500.00,
                    "features": ["5 Werbekampagnen", "1 Monat", "Analyse"],
                    "offer_type": "premium"
                }
            ]
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Online Marketing Paket')


    def test_offer_patch_as_owner(self):
        pass
