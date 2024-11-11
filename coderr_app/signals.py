from django.db import transaction
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import UserProfile

@transaction.atomic
def create_guest_accounts(sender, **kwargs):
    """
    Erstellt Gastbenutzerkonten, falls diese noch nicht existieren.

    Diese Funktion wird normalerweise von einem Signal aufgerufen, um sicherzustellen,
    dass bestimmte Gastbenutzerkonten automatisch erstellt werden, wenn das System
    gestartet wird. Die Funktion überprüft, ob die Benutzer mit den Benutzernamen 
    'andrey' und 'kevin' bereits existieren. Wenn nicht, werden sie mit vordefinierten 
    Daten erstellt und ein entsprechendes Benutzerprofil wird angelegt.

    Die Funktion wird nur ausgeführt, wenn die Anwendung nicht im TESTING-Modus läuft.

    Args:
        sender: Das sendende Signal, normalerweise das Modell, das das Signal auslöst.
        **kwargs: Zusätzliche Schlüsselwortargumente, die an das Signal übergeben werden.

    Returns:
        None: Diese Funktion gibt keinen Wert zurück. Sie hat jedoch Seiteneffekte, 
        indem sie Benutzerkonten erstellt und in der Datenbank speichert.

    Side Effects:
        - Erstellt zwei Gastbenutzerkonten in der Datenbank (Andrey und Kevin),
          sofern diese nicht bereits vorhanden sind.
        - Erstellt entsprechende Benutzerprofile für die Gastbenutzer.
    """
    if settings.TESTING:
        return

    User = get_user_model()

    for username in ['andrey', 'kevin']:
        try:
            user = User.objects.get(username=username)
            user.delete()
            print(f'Guestuser deleted: {username}')
        except User.DoesNotExist:
            print(f'Guestuser not found: {username}')

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
        UserProfile.objects.create(user=business, email=business.email, type='business', tel='49123456789', working_hours='9-17', description='Test Business User Developer', location='Testlocation')
        print(f'Business Guestuser created: {business}')
