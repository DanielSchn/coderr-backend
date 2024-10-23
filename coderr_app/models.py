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