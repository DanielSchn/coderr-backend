from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from coderr_app.models import UserProfile, Offers, OfferDetails, Orders
from rest_framework.authtoken.models import Token


class OrderCountTest(APITestCase):

    def setUp(self):
        self.business = User.objects.create_user(username='testuser', password='testpassword', email='test@test.de')
        self.user_profile = UserProfile.objects.create(user=self.business, email=self.business.email, type='business')
        self.admin = User.objects.create_superuser(username='admin', password='admin')
        self.customer = User.objects.create_user(username='testcustomer', password='testpassword', email='customer@test.de')
        self.user_profile_customer = UserProfile.objects.create(user=self.customer, email=self.customer.email, type='customer')

        self.offer = Offers.objects.create(
            user=self.business,
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
        self.order1 = Orders.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            offer=self.offer,
            offer_details=self.detail1,
            title=self.detail1.title,
            revisions=self.detail1.revisions,
            delivery_time_in_days=self.detail1.delivery_time_in_days,
            price=self.detail1.price,
            features=self.detail1.features,
            offer_type=self.detail1.offer_type,
            status='in_progress'
        )
        self.order2 = Orders.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            offer=self.offer,
            offer_details=self.detail2,
            title=self.detail2.title,
            revisions=self.detail2.revisions,
            delivery_time_in_days=self.detail2.delivery_time_in_days,
            price=self.detail2.price,
            features=self.detail2.features,
            offer_type=self.detail2.offer_type,
            status='in_progress'
        )
        self.order3 = Orders.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            offer=self.offer,
            offer_details=self.detail3,
            title=self.detail3.title,
            revisions=self.detail3.revisions,
            delivery_time_in_days=self.detail3.delivery_time_in_days,
            price=self.detail3.price,
            features=self.detail3.features,
            offer_type=self.detail3.offer_type,
            status='completed'
        )

        self.business_token = Token.objects.create(user=self.business)
        self.admin_token = Token.objects.create(user=self.admin)
        self.customer_token = Token.objects.create(user=self.customer)
        self.client = APIClient()


    def test_count_completed_order_as_customer(self):
        url = reverse('completed-order-count', kwargs={'business_user_id': self.business.id})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 1)


    def test_count_completed_order_as_business(self):
        url = reverse('completed-order-count', kwargs={'business_user_id': self.business.id})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 1)


    def test_count_completed_order_as_admin(self):
        url = reverse('completed-order-count', kwargs={'business_user_id': self.business.id})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 1)

    
    def test_count_completed_order_as_unauthorized(self):
        url = reverse('completed-order-count', kwargs={'business_user_id': self.business.id})

        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_count_order_as_customer(self):
        url = reverse('order-count', kwargs={'business_user_id': self.business.id})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 2)


    def test_count_order_as_business(self):
        url = reverse('order-count', kwargs={'business_user_id': self.business.id})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 2)


    def test_count_order_as_admin(self):
        url = reverse('order-count', kwargs={'business_user_id': self.business.id})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 2)

    
    def test_count_order_as_unauthorized(self):
        url = reverse('order-count', kwargs={'business_user_id': self.business.id})

        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)