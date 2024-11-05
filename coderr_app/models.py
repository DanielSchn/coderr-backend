from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Erweiterung des Standard-Benutzermodells für zusätzliche Informationen über den Benutzer.

    Attributes:
        user (User): Verknüpft das Benutzerprofil mit dem Django-Benutzermodell.
        file (FileField): Optionales Profilbild des Benutzers.
        location (str): Standort des Benutzers, max. 100 Zeichen.
        tel (str): Telefonnummer des Benutzers, max. 25 Zeichen.
        description (TextField): Beschreibung oder Biografie des Benutzers.
        working_hours (str): Arbeitszeiten des Benutzers.
        type (str): Benutzertyp, entweder 'customer', 'business' oder 'staff'.
        email (EmailField): E-Mail-Adresse des Benutzers.
        created_at (DateTimeField): Datum und Uhrzeit der Erstellung des Profils.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=100)
    tel = models.CharField(max_length=25)
    description = models.TextField()
    working_hours = models.CharField(max_length=25)
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
        ('staff', 'Staff')
    ]
    type = models.CharField(max_length=25, choices=USER_TYPE_CHOICES)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['user__username']
        verbose_name_plural = 'User Profiles'


class Offers(models.Model):
    """
    Repräsentiert ein Angebot, das ein Benutzer erstellen kann.

    Attributes:
        user (User): Der Benutzer, der das Angebot erstellt hat.
        title (str): Titel des Angebots, max. 150 Zeichen.
        image (FileField): Optionales Bild des Angebots.
        description (TextField): Beschreibung des Angebots.
        created_at (DateTimeField): Erstellungsdatum des Angebots.
        updated_at (DateTimeField): Letzte Aktualisierung des Angebots.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=150)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Offers'



class OfferDetails(models.Model):
    """
    Details eines spezifischen Angebots, z. B. Preis und Typ.

    Attributes:
        offer (Offers): Referenz auf das zugehörige Angebot.
        title (str): Titel des Angebotsdetails, max. 150 Zeichen.
        revisions (int): Anzahl der zulässigen Überarbeitungen, Standard: -1 (unbegrenzt).
        delivery_time_in_days (int): Lieferzeit in Tagen.
        price (DecimalField): Preis für dieses Detailpaket.
        features (JSONField): JSON-Daten für spezifische Merkmale oder Eigenschaften.
        offer_type (str): Typ des Angebotsdetails, entweder 'basic', 'standard' oder 'premium'.
    """
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=150)
    revisions = models.IntegerField(default=-1)
    delivery_time_in_days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ]
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPES)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Offerdetails'
    

class Orders(models.Model):
    """
    Repräsentiert eine Bestellung, die ein Kunde bei einem Anbieter tätigt.

    Attributes:
        customer_user (User): Der Kunde, der die Bestellung aufgibt.
        business_user (User): Der Anbieter, bei dem die Bestellung aufgegeben wird.
        offer (Offers): Das Angebot, das bestellt wird.
        offer_details (OfferDetails): Details zum spezifischen Angebot.
        title (str): Titel der Bestellung.
        revisions (int): Anzahl der Überarbeitungen in der Bestellung.
        delivery_time_in_days (int): Lieferzeit in Tagen.
        price (DecimalField): Preis für die Bestellung.
        features (JSONField): Merkmale der Bestellung im JSON-Format.
        offer_type (str): Typ des bestellten Angebots.
        created_at (DateTimeField): Erstellungsdatum der Bestellung.
        updated_at (DateTimeField): Datum der letzten Aktualisierung.
        status (str): Status der Bestellung, z. B. 'open', 'completed', etc.
    """
    customer_user = models.ForeignKey(User, related_name='customer_order', on_delete=models.CASCADE, limit_choices_to={'user_profile__type': 'customer'})
    business_user = models.ForeignKey(User, related_name='business_order', on_delete=models.CASCADE, limit_choices_to={'user_profile__type': 'business'})
    offer = models.ForeignKey('Offers', on_delete=models.CASCADE, related_name='orders')
    offer_details = models.ForeignKey('OfferDetails', on_delete=models.CASCADE, related_name='orders')
    title = models.CharField(max_length=150)
    revisions = models.IntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=25)

    def __str__(self):
        return f'Order by {self.customer_user.username} for {self.title}'
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Orders'
    

class Reviews(models.Model):
    """
    Repräsentiert eine Bewertung, die ein Kunde für ein Angebot hinterlässt.

    Attributes:
        customer_user (User): Der Kunde, der die Bewertung abgibt.
        business_user (User): Der Anbieter, der die Bewertung erhält.
        rating (int): Bewertungsskala, z. B. von 1 bis 5.
        description (TextField): Kommentar zur Bewertung.
        created_at (DateTimeField): Erstellungsdatum der Bewertung.
        updated_at (DateTimeField): Datum der letzten Aktualisierung.
    """
    customer_user = models.ForeignKey(User, related_name='customer_reviews', on_delete=models.CASCADE, limit_choices_to={'user_profile__type': 'customer'})
    business_user = models.ForeignKey(User, related_name='business_reviews', on_delete=models.CASCADE, limit_choices_to={'user_profile__type': 'business'})
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review for {self.business_user} by {self.customer_user}'
    
    class Meta:
        ordering = ['rating']
        verbose_name_plural = 'Reviews'