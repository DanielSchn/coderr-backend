from django.db import transaction
from django.contrib.auth import get_user_model
from .models import UserProfile

@transaction.atomic
def create_guest_accounts(sender, **kwargs):
    User = get_user_model()

    if not User.objects.filter(username='andrey').exists():
        customer = User.objects.create_user(
            username='andrey',
            password='asdasd',
            email='andrey@customer.de',
            first_name='Andrey',
            last_name='Customerguest'
        )
        UserProfile.objects.create(user=customer, email=customer.email, type='customer')
        print(f'Customer Guestuser created: {customer}')

    if not User.objects.filter(username='kevin').exists():
        business = User.objects.create_user(
            username='kevin',
            password='asdasd',
            email='kevin@business.de',
            first_name='Kevin',
            last_name='Businessguest'
        )
        UserProfile.objects.create(user=business, email=business.email, type='business')
        print(f'Business Guestuser created: {business}')
