from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from coderr_app.models import UserProfile, Offers, OfferDetails
from rest_framework.authtoken.models import Token


class OrdersTest(APITestCase):

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

        self.business_token = Token.objects.create(user=self.business)
        self.admin_token = Token.objects.create(user=self.admin)
        self.customer_token = Token.objects.create(user=self.customer)
        self.client = APIClient()


    def test_post_order_as_customer(self):
        url = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_order_as_business(self):
        url = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_post_order_as_admin(self):
        url = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_patch_order_as_business(self):
        url_patch = reverse('orders-detail', kwargs={'pk': 1})
        url_post = reverse('orders-list')
        data_post = {
            "offer_detail_id": 1
        }
        data_patch = {
            "status": "completed"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url_post, data_post, format='json')
        self.client.credentials()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response_patch = self.client.patch(url_patch, data_patch, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(response_patch.data['status'], 'completed')


    def test_patch_order_as_customer(self):
        url_patch = reverse('orders-detail', kwargs={'pk': 1})
        url_post = reverse('orders-list')
        data_post = {
            "offer_detail_id": 1
        }
        data_patch = {
            "status": "completed"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url_post, data_post, format='json')
        response_patch = self.client.patch(url_patch, data_patch, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_patch.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_patch_order_as_admin(self):
        url_patch = reverse('orders-detail', kwargs={'pk': 1})
        url_post = reverse('orders-list')
        data_post = {
            "offer_detail_id": 1
        }
        data_patch = {
            "status": "completed"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url_post, data_post, format='json')
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response_patch = self.client.patch(url_patch, data_patch, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)


    def test_get_orders_as_business(self):
        url = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url, data, format='json')
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response_get = self.client.get(url)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)


    def test_get_orders_as_customer(self):
        url = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url, data, format='json')
        response_get = self.client.get(url)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)


    def test_get_orders_as_admin(self):
        url = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url, data, format='json')
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response_get = self.client.get(url)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)


    def test_get_order_detail_as_business(self):
        url_get = reverse('orders-detail', kwargs={'pk': 1})
        url_post = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url_post, data, format='json')
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response_get = self.client.get(url_get)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)


    def test_get_order_detail_as_customer(self):
        url_get = reverse('orders-detail', kwargs={'pk': 1})
        url_post = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url_post, data, format='json')
        response_get = self.client.get(url_get)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)


    def test_get_order_detail_as_admin(self):
        url_get = reverse('orders-detail', kwargs={'pk': 1})
        url_post = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url_post, data, format='json')
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response_get = self.client.get(url_get)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)


    def test_delete_order_as_business(self):
        url_delete = reverse('orders-detail', kwargs={'pk': 1})
        url_post = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url_post, data, format='json')
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response_get = self.client.delete(url_delete)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_order_as_customer(self):
        url_delete = reverse('orders-detail', kwargs={'pk': 1})
        url_post = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url_post, data, format='json')
        response_get = self.client.delete(url_delete)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_delete_order_as_admin(self):
        url_delete = reverse('orders-detail', kwargs={'pk': 1})
        url_post = reverse('orders-list')
        data = {
            "offer_detail_id": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response_post = self.client.post(url_post, data, format='json')
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response_get = self.client.delete(url_delete)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_204_NO_CONTENT)