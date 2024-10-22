from rest_framework import serializers
from coderr_app.models import UserProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = [
            'user', 'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at'
        ]
        read_only_fields = ['created_at']