from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from coderr_app.models import UserProfile, Offers, OfferDetails, Orders, Reviews
from coderr_app.example_data import EXAMPLE_BUSINESS_USERS, EXAMPLE_CUSTOMERS, EXAMPLE_OFFERS
from django.core.management import call_command
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populiert die Datenbank mit Testdaten für ein Fiverr-ähnliches System'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Flushe die gesamte Datenbank...'))
        call_command('flush', interactive=False)
        self.stdout.write(self.style.SUCCESS('Datenbank erfolgreich zurückgesetzt.'))

        business_users = {}
        for data in EXAMPLE_BUSINESS_USERS:
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            UserProfile.objects.create(
                user=user,
                location=data['location'],
                tel=data['tel'],
                description=data['description'],
                working_hours=data['working_hours'],
                type='business',
                email=data['email'],
                file=data['file']
            )
            business_users[data['username']] = user

        self.stdout.write(self.style.SUCCESS(
            f'{len(business_users)} Business User erfolgreich erstellt.'))

        customers = []
        for data in EXAMPLE_CUSTOMERS:
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            UserProfile.objects.create(
                user=user,
                location=data['location'],
                tel=data['tel'],
                description=data['description'],
                type='customer',
                email=data['email'],
                file=data['file']
            )
            customers.append(user)

        self.stdout.write(self.style.SUCCESS(
            f'{len(customers)} Customers erfolgreich erstellt.'))

        offers = []
        for username, offer_list in EXAMPLE_OFFERS.items():
            user = business_users[username]
            for offer_data in offer_list:
                offer = Offers.objects.create(
                    user=user,
                    title=offer_data['title'],
                    description=offer_data['description'],
                    image=offer_data['image']
                )
                for detail in offer_data['details']:
                    OfferDetails.objects.create(
                        offer=offer,
                        title=f'{
                            offer.title} - {detail["offer_type"].capitalize()}',
                        revisions=detail['revisions'],
                        delivery_time_in_days=detail['delivery_time_in_days'],
                        price=Decimal(detail['price']),
                        features=detail['features'],
                        offer_type=detail['offer_type']
                    )
                offers.append(offer)

        self.stdout.write(self.style.SUCCESS(
            f'{len(offers)} Angebote erfolgreich erstellt.'))

        for customer in customers:
            for offer in offers:
                offer_details = offer.details.first()
                Orders.objects.create(
                    customer_user=customer,
                    business_user=offer.user,
                    offer=offer,
                    offer_details=offer_details,
                    title=f'Bestellung von {
                        customer.username} für {offer.title}',
                    revisions=1,
                    delivery_time_in_days=offer_details.delivery_time_in_days,
                    price=offer_details.price,
                    features=offer_details.features,
                    offer_type=offer_details.offer_type,
                    status='completed'
                )

        self.stdout.write(self.style.SUCCESS(
            'Bestellungen erfolgreich erstellt.'))

        for customer in customers:
            for business_user in business_users.values():
                Reviews.objects.create(
                    customer_user=customer,
                    business_user=business_user,
                    rating=random.randint(3, 5),
                    description=f'Tolle Arbeit von {business_user.username}.'
                )

        self.stdout.write(self.style.SUCCESS(
            'Bewertungen erfolgreich erstellt.'))
