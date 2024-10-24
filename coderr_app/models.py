from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=100)
    tel = models.CharField(max_length=25)
    description = models.TextField()
    working_hours = models.CharField(max_length=25)
    type = models.CharField(max_length=25)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['user__username']


class Offers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=150)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    min_delivery_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    @property
    def min_price(self):
        details = self.details.all()
        return min((detail.price for detail in details), default=0.00)

    @property
    def min_delivery_time(self):
        details = self.details.all()
        return min((detail.delivery_time_in_days for detail in details), default=0)


class OfferDetails(models.Model):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=150)
    revisions = models.IntegerField(default=-1)
    delivery_time_in_days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=50)

    def __str__(self):
        return self.title